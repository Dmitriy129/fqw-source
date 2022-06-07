import os
import re
from src.GitHub import GithubClient
from src.GoogleSheets import GoogleSheetClient
from src.Moodle import MoodleClient


def getAllClientsOld(config):
    if(not config):
        raise "empty config"
    # git - ok
    ghclient = GithubClient(config["github"]["credentials"]["accessToken"])

    # google sheets - ok
    gsclient = GoogleSheetClient(config["googleSheet"]["id"])

    # moodle - ok
    mdclient = MoodleClient(
        baseUrl=config["moodle"]["baseUrl"],
        token=config["moodle"]["credentials"]["token"])

    return ghclient, gsclient, mdclient


def getAllClients(config):
    if(not config):
        raise "empty config"
    # git - ok
    ghclient = GithubClient(os.environ['GITHUB_ACCESS_TOKEN'])

    # google sheets - ok
    gsclient = GoogleSheetClient(config["googleSheet"]["id"])

    # moodle - ok
    mdclient = MoodleClient(
        baseUrl=config["moodle"]["baseUrl"],
        token=os.environ['MOODLE_ACCESS_TOKEN'])

    return ghclient, gsclient, mdclient


def longFioToShortFio(fioLong):
    arrFioLong = fioLong.split(" ")
    fioShort = " ".join([arrFioLong[1], arrFioLong[0]])
    return fioShort


def getDictPRGradeInfo(dictFioGradeInfo, dictFioGit, dictGitPR):
    dicPrGradeInfo = {}
    for fioLong in dictFioGit:
        if not fioLong:
            continue
        git = dictFioGit[fioLong]
        fioShort = longFioToShortFio(fioLong)
        if fioShort in dictFioGradeInfo and git in dictGitPR:
            grade = dictFioGradeInfo[fioShort]
            pr = dictGitPR[git]
            dicPrGradeInfo[pr] = grade
    return dicPrGradeInfo


def getGradeByPR(dictFioGradeInfo, dictGitFio, pr):
    if pr.user.login in dictGitFio:
        fioLong = dictGitFio[pr.user.login]
        fioShort = longFioToShortFio(fioLong)
        if(fioShort in dictFioGradeInfo):
            return dictFioGradeInfo[fioShort]
    return None


def genLabelByGrade(raw, min, max, labelConfig):
    # percent = raw/max*100
    percentConfig = labelConfig["config"]
    defaultTemplate = labelConfig["defaultTemplate"]
    defaultColor = labelConfig["defaultColor"]

    percent = (raw-min)/(max-min)*100
    for [[pMin, pMax], conf] in percentConfig:
        if percent >= pMin and percent <= pMax:
            name = f'{defaultTemplate} {conf["template"].format(raw=raw, min=min, max=max)}'
            color = conf["color"]
            description = None
            comment = None
            needToClose = False
            if "description" in conf:
                description = conf["description"].format(
                    raw=raw, min=min, max=max)
            if "comment" in conf:
                comment = conf["comment"].format(raw=raw, min=min, max=max)
            if "needToClose" in conf:
                needToClose = conf["needToClose"]
            return name, color, description, comment, needToClose
    return f'{defaultTemplate}: error', defaultColor, "", "Обратитесь к преподавателю.", None


# add grade labels to prs
def addGradeLabelToPR(dictPRGradeInfo, labelConfig):
    for pr in dictPRGradeInfo:
        grade = dictPRGradeInfo[pr]
        addLabelToPRByGrade(pr, grade, labelConfig)


def addLabelToPRByGrade(pr, grade, labelConfig):
    name, color, description, comment, needToClose = genLabelByGrade(
        raw=grade["raw"],
        min=grade["min"],
        max=grade["max"],
        labelConfig=labelConfig)

    oldLabel = next(
        (l for l in pr.labels
         if labelConfig["defaultTemplate"] in l.name),        None)
    if oldLabel:
        oldLabel.edit(name=name,
                      color=color,
                      description=description)
    else:
        pr.add_to_labels(name)
        newLabel = next((l for l in pr.labels if l.name == name), None)
        if newLabel:
            newLabel.edit(name=newLabel.name,
                          color=color,
                          description=description)
    if comment:
        pr.create_issue_comment(comment)
    if needToClose:
        pr.edit(state="closed")


def addLabelToPRsByGrade(dictPRGradeInfo, labelConfig):
    for pr in dictPRGradeInfo:
        grade = dictPRGradeInfo[pr]
        addLabelToPRByGrade(pr, grade, labelConfig)


def chooseMoodleRunConfigByPrTitle(moodleRunConfigs, prTitle):
    return next((moodleRunConfig for moodleRunConfig in moodleRunConfigs if re.search(
        moodleRunConfig["prRegex"], prTitle) != None), None)
