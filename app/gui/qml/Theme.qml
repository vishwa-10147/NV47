pragma Singleton
import QtQuick

QtObject {
    // Backgrounds
    readonly property color bgDark: "#050b14"
    readonly property color panelBg: "#0d1627"
    readonly property color panelBgTransparent: Qt.rgba(13/255, 22/255, 39/255, 0.8)
    
    // Accents
    readonly property color accentPrimary: "#00d2ff"
    readonly property color accentSecondary: "#8a2be2" // Violet
    readonly property color border: "#1e293b"
    
    // Status Colors
    readonly property color success: "#10b981"
    readonly property color warning: "#f59e0b"
    readonly property color error: "#ef4444"
    
    // Text
    readonly property color textMain: "#ffffff"
    readonly property color textDim: "#94a3b8"
    
    // Metrics
    readonly property int radius: 8
    readonly property int spacing: 15
}
