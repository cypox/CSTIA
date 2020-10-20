'use strict'
const electron = require("electron")
const mousetrap = require("mousetrap")
const currentWindow = electron.remote.getCurrentWindow()
const api = electron.remote.getGlobal("api")
const { v4: uuidv4 } = require('uuid');

function getElectronVersion() {
	return (process.versions.electron)
}
function getNodejsVersion() {
	return (process.versions.node)
}
function changeFullScreenState() {
	currentWindow.setFullScreen(!currentWindow.isFullScreen())
}
function reloadBrowserWindow() {
	currentWindow.reload()
}
function closeBrowserWindow() {
	window.close()
}
async function changeTitle(title){
	document.title = title
}
function getRandomNetworkKey() {
	return uuidv4()
}
function makeReport(sServerName,
	sSanctionType,
	sTargetAccountPseudo,
	sTargetAccountId,
	sSanctionnatedAccounts,
	sDescription,
	sFindAccounts,
	sPenal,
	sJailDialog,
	sComplementary) {
	api.reportMaker.makeReport(sServerName, sSanctionType, sTargetAccountPseudo, sTargetAccountId, sSanctionnatedAccounts, stripHtml(sDescription), stripHtml(sFindAccounts), stripHtml(sPenal), stripHtml(sJailDialog), stripHtml(sComplementary))
}
function makeLog(sLogFile, sMessage, bError)
{
	if (bError == null) bError = false
	var date = new Date
	var hours = date.getHours()
	var minutes = date.getMinutes()
	var seconds = date.getSeconds()
	var milliSeconds = date.getMilliseconds()
	while (String(hours).length < 2)
	{
		hours = "0" + hours
	}
	while (String(minutes).length < 2)
	{
		minutes = "0" + minutes
	}
	while (String(seconds).length < 2)
	{
		seconds = "0" + seconds
	}
	while (String(milliSeconds).length < 3)
	{
		milliSeconds = "0" + milliSeconds
	}
	var sTime = "[" + hours + ":" + minutes + ":" + seconds + ":" + milliSeconds + "] "
	sMessage = sTime + sMessage
	if (bError)
	{
		console.error(sMessage)
	}
	else
	{
		console.log(sMessage)
	}
	if (sLogFile == null)
	{
		return
	}
	api.utils.writeLog(sLogFile, sMessage)
}

function stripHtml(html){
    // Create a new div element
    var temporalDivElement = document.createElement("div")
    // Set the HTML content with the providen
    temporalDivElement.innerHTML = html
    // Retrieve the text property of the element (cross-browser support)
    return temporalDivElement.textContent || temporalDivElement.innerText || ""
}

var _aPendingConsoleLogs = new Array()
var _nGroupConsoleLogsTimeout

function printPendingConsoleLogs()
{
	if (_aPendingConsoleLogs.length == 0) {
		return
	}
	for (var i = 0; i < _aPendingConsoleLogs.length; i++) {
		var oPendingConsoleLogsGroup = _aPendingConsoleLogs[i]
		makeLog("console", oPendingConsoleLogsGroup.sMessage, oPendingConsoleLogsGroup.bError)
	}
	_aPendingConsoleLogs = new Array()
}

function consoleLog(sType, sServerText)
{
	var sMessage = stripHtml(sServerText)
	var bError = sType == "DEBUG_ERROR"
	var bLastOneSimilar = false
	if (_aPendingConsoleLogs.length > 0) {
		var oPendingConsoleLogsGroup = _aPendingConsoleLogs[_aPendingConsoleLogs.length - 1]
		if (oPendingConsoleLogsGroup.bError == bError) {
			// Si le type est similaire, on append (on maintient l'ordre des groupements)
			bLastOneSimilar = true
			oPendingConsoleLogsGroup.sMessage += "\n" + sMessage // Si trouvé, on append le texte
		}
	}
	if (!bLastOneSimilar) {
		// S'il n'existe pas ou que le statut erreur a changé, on push dans l'array
		_aPendingConsoleLogs.push({sMessage : sMessage, bError:bError})
	}
	if (_nGroupConsoleLogsTimeout != undefined) {
		clearTimeout(_nGroupConsoleLogsTimeout)
	}
	var nTimeout = setTimeout(function(){
	    printPendingConsoleLogs() // Sera exécuté dans 50ms si aucun autre log n'arrive avant
	}, 50)
	_nGroupConsoleLogsTimeout = nTimeout
}
function chatLog(sText)
{
	var sMessage = stripHtml(sText)
	makeLog("chat", sMessage)
}
function userLog(sMessage, bError)
{
	var sMessage
	var sType = "[CLIENT"
	if (bError)
	{
		sType = sType + "_ERROR] "
	}
	else
	{
		sType = sType + "] "
	}
	sMessage = sType + sMessage
	makeLog("user", sMessage, bError)
}
function debugRequest(bSend, bLogToFile, sData, sPlayerName, sCurrentServer) {
	var sArrow
	var sMessage
	if (bSend)
	{
		sArrow = "--> "
	}
	else
	{
		sArrow = "<-- "
	}
	if (sPlayerName == null)
	{
		sMessage = sArrow + sData
	}
	else
	{
		sMessage = "(" + sPlayerName + ", " + sCurrentServer + ") " + sArrow + sData
	}
	makeLog(bLogToFile ? "requests" : null, sMessage)
}
async function makeNotification(body){
	var focusedWindow = electron.remote.BrowserWindow.getFocusedWindow()
	if (focusedWindow != null) {
		return
	}
	// Si Dofus 1 est en arrière plan
	if (!api.config.get("bBackgroundNotifications")) {
		return
	}
	var n = new Notification(document.title, {
		body: body
	})
}

async function setIngameDiscordActivity(sVersion, sCurrentServer, sPlayerName, sAccountPseudo, sGuildName, nGuild, nSex) {
	api.game.setIngameDiscordActivity(sVersion, sCurrentServer, sPlayerName, sAccountPseudo, sGuildName, nGuild, nSex)
}

async function setLoginDiscordActivity(sVersion, sVersionDate) {
	api.game.setLoginDiscordActivity(sVersion, sVersionDate)
}

function focusGame() {
	document.getElementById("flashGame").focus()
}

function onGameFocus() {
	document.getElementById("flashGame").onWindowFocus()
}

function onGameBlur() {
	if (!api.config.get("bMultiAccountOptimisation")) {
		return
	}
	document.getElementById("flashGame").onWindowBlur()
}

focusGame()

document.getElementById("flashGame").oncontextmenu = function(e) {
	e.preventDefault()
	document.getElementById("flashGame").onRightClick()
}

window.addEventListener("focus", onGameFocus, false);
window.addEventListener("blur", onGameBlur, false);

Mousetrap.bind("tab", () => {
	if (!api.config.get("bTabKey")) {
	  // Désactive la touche TAB, pose des soucis dans les raccourcis jeu
	  return false
	}
})	

Mousetrap.bind((process.platform == "darwin" ? "command" : "ctrl") + "+q", () => {
  closeBrowserWindow()
  return false
})

Mousetrap.bind((process.platform == "darwin" ? "command" : "ctrl") + "+r", () => {
  reloadBrowserWindow()
  return false
})

Mousetrap.bind((process.platform == "darwin" ? "command" : "ctrl") + "+f", () => {
  changeFullScreenState()
  return false
})

if (process.platform != "darwin")
{
	Mousetrap.bind("alt+f4", () => {
	  closeBrowserWindow()
	  return false
	})
}