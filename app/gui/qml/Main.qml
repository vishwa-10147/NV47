import QtQuick
import QtQuick.Controls
import QtQuick.Window

ApplicationWindow {
    id: root
    visible: true
    width: 1280
    height: 720
    title: "NV001 Intelligence"
    color: "#050b14"

    Rectangle {
        anchors.centerIn: parent
        width: 400
        height: 200
        color: "#0d1627"
        border.color: "#00d2ff"
        border.width: 1
        radius: 10

        Column {
            anchors.centerIn: parent
            spacing: 20

            Text {
                text: "NV001 PySide6 GUI Initialized"
                color: "#00d2ff"
                font.pixelSize: 18
                font.bold: true
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: typeof backend !== "undefined" ? backend.get_system_status() : "Backend disconnected"
                color: "#10b981"
                font.pixelSize: 14
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }
}
