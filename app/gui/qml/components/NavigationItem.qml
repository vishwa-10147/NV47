import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: parent.width
    height: 50
    
    property string iconSource: ""
    property string text: ""
    property bool isActive: false
    
    signal clicked()
    
    Rectangle {
        id: bg
        anchors.fill: parent
        color: root.isActive ? Qt.rgba(0, 210, 255, 0.1) : (mouseArea.containsMouse ? Qt.rgba(0, 210, 255, 0.05) : "transparent")
        
        Rectangle {
            width: 3
            height: parent.height
            anchors.left: parent.left
            color: root.isActive ? Theme.accentPrimary : "transparent"
        }
        
        Row {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 20
            spacing: 15
            
            Image {
                source: root.iconSource
                width: 20
                height: 20
                sourceSize: Qt.size(20, 20)
                opacity: root.isActive ? 1.0 : (mouseArea.containsMouse ? 0.8 : 0.6)
                
                // Pure white icon colored by QML ColorOverlay if wanted, 
                // but since our SVG uses currentColor, we'll map color in a basic way:
            }
            
            Text {
                text: root.text
                color: root.isActive ? Theme.accentPrimary : (mouseArea.containsMouse ? Theme.textMain : Theme.textDim)
                font.pixelSize: 14
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }
}
