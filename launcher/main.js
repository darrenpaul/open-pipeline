const url = require("url")
const path = require("path")
const electron = require("electron")

const {app, BrowserWindow} = electron

let mainWindow

app.on("ready", function(){
    mainWindow = new BrowserWindow({})

    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, "home.html"),
        protocol: "file:",
        slashes: true
    }))
})
