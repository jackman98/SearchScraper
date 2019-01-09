import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import SearchTypes 1.0

ApplicationWindow {
    id: root

    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    StackView {
        id: stackView

        anchors.fill: parent

        initialItem: RowLayout {

            TextField {
                id: _inputField

                Layout.alignment: Qt.AlignCenter
                placeholderText: qsTr("Введите поисковый запрос")
            }

            Button {

                Layout.alignment: Qt.AlignCenter
                text: qsTr("Поиск")

                onClicked: {
                    searchEngine.searchTextByAllEngines(_inputField.text)
                    stackView.push(searchEngines);
                }
            }
        }
    }

    Connections {
        target: searchEngine

        onResultReceived: {
            switch(searchEngineName) {
            case _google.objectName:
                break;
            case _yandex.objectName:
                break;
            case _bing.objectName:

                break;
            case _yahoo.objectName:

                break;
            case _duckduckgo.objectName:

                break;
            }
        }
    }

    Page {
        id: searchEngines

        visible: false

        SwipeView {
            id: swipeView

            anchors.fill: parent

            currentIndex: bar.currentIndex

            ListView {
                id: _google
                objectName: "google"

                model: searchEngine.google.links

                delegate: Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: name
                }
            }
            ListView {
                id: _yandex
                objectName: "yandex"

                model: searchEngine.yandex.links

                delegate: Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: name
                }
            }
            ListView {
                id: _bing
                objectName: "bing"

                model: searchEngine.bing.links

                delegate: Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: name
                }
            }
            ListView {
                id: _yahoo
                objectName: "yahoo"

                model: searchEngine.yahoo.links

                delegate: Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: name
                }
            }
            ListView {
                id: _duckduckgo
                objectName: "duckduckgo"

                model: searchEngine.duckduckgo.links

                delegate: Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: name
                }
            }
        }

        footer: TabBar {
            id: bar

            width: parent.width
            position: TabBar.Footer
            currentIndex: swipeView.currentIndex

            TabButton {
                text: qsTr("Google")
            }
            TabButton {
                text: qsTr("Yandex")
            }
            TabButton {
                text: qsTr("Bing")
            }
            TabButton {
                text: qsTr("Yahoo")
            }
            TabButton {
                text: qsTr("Duckduckgo")
            }
        }
    }
}
