var fs = require('fs');
var path = require('path');
var homedir = require('os').homedir();
var tempDir = require('os').tmpdir();
var PythonShell = require('python-shell');
const remote = require('electron').remote;

// Loop through all the files in the temp directory

// jsonPath = path.join(tempDir, "open_pipeline", ".environment_data.json")

var _applicationConfigPath = path.join(tempDir, "open_pipeline", "applications")


function Check_Applications(){
    fs.readdir(_applicationConfigPath, function(_error, files){
        console.log(_applicationConfigPath)
        if(_error){
            console.error("Could not list the directory.", _error)
            process.exit(1)
        } 
    
        files.forEach( function(file, index){
            let appData = require(path.join(_applicationConfigPath, file))
            Add_Application(appData)
        })
    })
}


// Added the application objects to the html.
function Add_Application(object){
    console.log(object)

    var appSelection = document.getElementById("application-selection")

    var columnDiv = document.createElement("div")
    columnDiv.className = "col-sm-3 application-space"
    appSelection.appendChild(columnDiv)

    var appIconAnchor = document.createElement("a")
    appIconAnchor.href = "#"
    columnDiv.appendChild(appIconAnchor)
    var appIcon = document.createElement("img")
    appIcon.src = object.icon
    appIcon.className = "img-responsive application-image"
    appIcon.alt = object.name
    appIconAnchor.appendChild(appIcon)

    var appNameAnchor = document.createElement("a")
    appNameAnchor.href = "#"
    appNameAnchor.className = "application-version"
    columnDiv.appendChild(appNameAnchor)
    var appName = document.createElement("h4")
    appName.innerText = object.name
    appNameAnchor.appendChild(appName)

    var dropDown = document.createElement("div")
    dropDown.className = "dropdown"
    columnDiv.appendChild(dropDown)

    var anchor = document.createElement("a")
    anchor.className = "dropdown-toggle application-version"
    anchor.id = object.name + "_version"
    anchor.innerText = "Version"
    anchor.setAttribute("data-toggle","dropdown");
    dropDown.appendChild(anchor)
    var anchorSpan = document.createElement("span")
    anchorSpan.className = "caret"
    anchor.appendChild(anchorSpan)

    var listGroup = document.createElement("ul")
    listGroup.className = "dropdown-menu application-version-dropdown"
    dropDown.appendChild(listGroup)
    
    object.versions.forEach( function(version, index){
        var list = document.createElement("li")
        listGroup.appendChild(list)
        var listAnchor = document.createElement("a")
        listAnchor.className = "application-version"
        listAnchor.href = "#"
        listAnchor.innerText = version
        listAnchor.onclick=function(){Update_Application_Version(anchor.id, version)};
        list.appendChild(listAnchor)
    })
    Update_Application_Version(anchor.id, object.versions[0])
    appIconAnchor.onclick=function(){Launch_Application(object.name, document.getElementById(anchor.id).innerText)};
    appNameAnchor.onclick=function(){Launch_Application(object.name, document.getElementById(anchor.id).innerText)};
}

function Update_Application_Version(element, value){
    element = document.getElementById(element)
    element.innerText = value
}

function Instantiate_Environment(){
    _environmentScriptPath = "C:/Users/darrenpaul/development/open-pipeline/environment/environment_core.py"

    PythonShell.run(_environmentScriptPath, function(err, results){
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log(results)
        Check_Applications()
    })
}

function Launch_Application(application_name, application_version){
    console.log("Launching " + application_name)
    console.log("Version: " + application_version)

    data = JSON.stringify({"product": application_name, "version": application_version})
    // Create_Json_Object()
    _environmentScriptPath = "C:/Users/darrenpaul/development/open-pipeline/environment/environment_core.py"
    
    var options = {
        mode: 'text',
        args: [data]
      };


    PythonShell.run(_environmentScriptPath, options, function(err, results){
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log(results);
      })
}

function Create_Json_Object(){
    // jsonPath = path.join(tempDir, "open_pipeline", ".environment_data.json")
    tempDirectory = path.join(tempDir, "open_pipeline")
    if(fs.existsSync(tempDirectory) == false){
        console.log("Creating temp directory for open pipeline data...")
        fs.mkdirSync(tempDirectory)
    }
    environmentData = path.join(tempDirectory, ".environment_data.json")
    fs.writeFile(environmentData, JSON.stringify({"fruit": "apples"}), function(err){
        if(err)
        throw err
    })
}

Instantiate_Environment()