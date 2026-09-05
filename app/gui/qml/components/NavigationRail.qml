import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    width: 220
    color: Theme.panelBg
    border.color: Theme.border
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        
        // Logo Area
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 140
            
            Column {
                anchors.centerIn: parent
                spacing: 5
                
                Image {
                    source: "file:app/gui/assets/icons/nv001-logo.svg"
                    width: 60
                    height: 60
                    anchors.horizontalCenter: parent.horizontalCenter
                    sourceSize: Qt.size(60, 60)
                }
                
                Text {
                    text: "NV001"
                    color: Theme.textMain
                    font.pixelSize: 20
                    font.bold: true
                    font.letterSpacing: 2
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Text {
                    text: "AUTONOMOUS INTELLIGENCE"
                    color: Theme.textDim
                    font.pixelSize: 8
                    font.letterSpacing: 1
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Text {
                    text: "LOCAL • SECURE • EVOLVING"
                    color: Theme.accentPrimary
                    font.pixelSize: 8
                    font.letterSpacing: 1
                    anchors.horizontalCenter: parent.horizontalCenter
                    opacity: 0.8
                }
            }
            
            Rectangle {
                width: parent.width
                height: 1
                color: Theme.border
                anchors.bottom: parent.bottom
            }
        }
        
        // Navigation Items
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            Column {
                width: parent.width
                anchors.top: parent.top
                anchors.topMargin: 15
                
                NavigationItem { text: "Home"; iconSource: "file:app/gui/assets/icons/navigation/home.svg"; isActive: true }
                NavigationItem { text: "Tasks"; iconSource: "file:app/gui/assets/icons/navigation/tasks.svg" }
                NavigationItem { text: "Tools"; iconSource: "file:app/gui/assets/icons/navigation/tools.svg" }
                NavigationItem { text: "Memory"; iconSource: "file:app/gui/assets/icons/navigation/memory.svg" }
                NavigationItem { text: "Knowledge"; iconSource: "file:app/gui/assets/icons/navigation/knowledge.svg" }
                NavigationItem { text: "Perception"; iconSource: "file:app/gui/assets/icons/navigation/perception.svg" }
                NavigationItem { text: "System"; iconSource: "file:app/gui/assets/icons/navigation/system.svg" }
                NavigationItem { text: "Settings"; iconSource: "file:app/gui/assets/icons/navigation/settings.svg" }
            }
        }
        
        // Bottom Status
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            
            Rectangle {
                width: parent.width
                height: 1
                color: Theme.border
                anchors.top: parent.top
            }
            
            Column {
                anchors.centerIn: parent
                spacing: 5
                
                Text {
                    text: "v1.0.0"
                    color: Theme.textDim
                    font.pixelSize: 10
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Row {
                    anchors.horizontalCenter: parent.horizontalCenter
                    spacing: 5
                    Rectangle {
                        width: 6; height: 6; radius: 3
                        color: Theme.success
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: "Kernel Online"
                        color: Theme.success
                        font.pixelSize: 10
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
            }
        }
    }
}
