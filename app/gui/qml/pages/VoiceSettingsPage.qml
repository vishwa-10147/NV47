import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../" // For Theme

Rectangle {
    id: root
    color: "transparent"
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20
        
        Text {
            text: "Voice Settings"
            color: Theme.accentPrimary
            font.pixelSize: 24
            font.bold: true
        }
        
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Theme.border
        }
        
        // Voice selection mock/demo UI
        RowLayout {
            spacing: 20
            
            Text {
                text: "Select Voice:"
                color: Theme.textMain
                font.pixelSize: 16
            }
            
            ComboBox {
                id: voiceCombo
                Layout.preferredWidth: 300
                model: typeof voiceBackend !== "undefined" ? voiceBackend.get_available_voices() : []
                textRole: "name"
                valueRole: "id"
                
                // Initialize to current config
                Component.onCompleted: {
                    if (typeof voiceBackend !== "undefined") {
                        let cfg = voiceBackend.get_config();
                        currentIndex = indexOfValue(cfg.voice_id);
                    }
                }
                
                onActivated: {
                    if (typeof voiceBackend !== "undefined") {
                        voiceBackend.update_setting("voice_id", currentValue);
                    }
                }
            }
        }
        
        RowLayout {
            spacing: 20
            
            Button {
                text: "Preview Voice"
                onClicked: {
                    if (typeof voiceBackend !== "undefined") {
                        voiceBackend.preview_voice("Hello, I am NV001. All systems are operating normally.");
                    }
                }
            }
            
            Button {
                text: "Stop Speaking"
                onClicked: {
                    if (typeof voiceBackend !== "undefined") {
                        voiceBackend.stop_speaking();
                    }
                }
            }
        }
        
        Item { Layout.fillHeight: true } // Spacer
    }
}
