import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import "components"

ApplicationWindow {
    id: root
    visible: true
    width: 1280
    height: 720
    title: "NV001 Intelligence"
    color: Theme.bgDark

    RowLayout {
        anchors.fill: parent
        anchors.margins: Theme.spacing
        spacing: Theme.spacing

        // Left Navigation
        NavigationRail {
            Layout.fillHeight: true
            Layout.preferredWidth: 220
        }

        // Center Content Placeholder
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Theme.panelBg
            border.color: Theme.border
            border.width: 1
            radius: Theme.radius

            Column {
                anchors.centerIn: parent
                spacing: 20

                Text {
                    text: "Main Dashboard Area (Coming Soon)"
                    color: Theme.accentPrimary
                    font.pixelSize: 18
                    font.bold: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    text: typeof backend !== "undefined" ? backend.get_system_status() : "Backend disconnected"
                    color: Theme.success
                    font.pixelSize: 14
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }
    }
}
