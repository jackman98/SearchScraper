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

        initialItem: ColumnLayout {
            id: _mainPage

            function changeSearcherStatus(name, status) {
                var listSearchers = searchEngine.searchersNames;
                if (status) {
                    listSearchers.push(name);
                }
                else {
                    for (var i = 0; i < listSearchers.length; i++) {
                        if (listSearchers[i] === name) {
                            listSearchers.splice(i, 1)
                        }
                    }
                }
                searchEngine.searchersNames = listSearchers;
            }

            RowLayout {

                Layout.alignment: Qt.AlignCenter

                GroupBox {
                    title: "Searchers"

                    Column {
                        spacing: 20

                        CheckBox {
                            text: qsTr("Google")
                            onCheckedChanged: {
                                _mainPage.changeSearcherStatus("google", checked);
                            }
                        }
                        CheckBox {
                            text: qsTr("Baidu")
                            onCheckedChanged: {
                                _mainPage.changeSearcherStatus("baidu", checked);
                            }
                        }
                        CheckBox {
                            text: qsTr("Bing")
                            onCheckedChanged: {
                                _mainPage.changeSearcherStatus("bing", checked);
                            }
                        }
                        CheckBox {
                            text: qsTr("Yahoo")
                            onCheckedChanged: {
                                _mainPage.changeSearcherStatus("yahoo", checked);
                            }
                        }
                        CheckBox {
                            text: qsTr("Duckduckgo")
                            onCheckedChanged: {
                                _mainPage.changeSearcherStatus("duckduckgo", checked);
                            }
                        }
                    }
                }

                GroupBox {
                    title: "Parameters"

                    Column {
                        spacing: 20

                        RowLayout {
                            Label {
                                Layout.alignment: Qt.AlignCenter

                                text: qsTr("Number pages for keyword")
                                horizontalAlignment: Label.AlignHCenter
                                verticalAlignment: Label.AlignVCenter
                            }
                            TextField {
                                id: _numberPagesForKeyword
                                Layout.alignment: Qt.AlignCenter

                                validator: IntValidator{bottom: 1; top: 30;}

                                placeholderText: qsTr("Default: 3")
                            }
                        }
                        Button {
                            text: qsTr("Test search")
                            onClicked: {
                                searchEngine.searchersNames = ["google", "baidu", "bing", "yahoo", "duckduckgo"];
                                searchEngine.numberPagesForKeyword = 1;
                                searchEngine.searchTextByAllEngines("hello");
                                stackView.push(searchEngines);
                            }
                        }
                    }
                }
            }

            RowLayout {

                Layout.alignment: Qt.AlignCenter

                TextField {
                    id: _inputField

                    Layout.alignment: Qt.AlignCenter
                    // placeholderText: qsTr("Enter search request")
                    text: "hello"
                }

                Button {

                    Layout.alignment: Qt.AlignCenter
                    text: qsTr("Search")

                    enabled: _inputField.length

                    onClicked: {

                        if (_numberPagesForKeyword.length > 0) {
                            searchEngine.numberPagesForKeyword = _numberPagesForKeyword.text;
                        }

                        searchEngine.searchTextByAllEngines(_inputField.text);
                        stackView.push(searchEngines);
                    }
                }
            }
        }
    }

    Page {
        id: searchEngines

        visible: false

        property var modelByName: {"google" : searchEngine.google.links,
            "baidu" : searchEngine.baidu.links,
            "bing" : searchEngine.bing.links,
            "yahoo" : searchEngine.yahoo.links,
            "duckduckgo" : searchEngine.duckduckgo.links
        }

        SwipeView {
            id: swipeView

            anchors.fill: parent

            currentIndex: bar.currentIndex

            Repeater {
                model: searchEngine.searchersNames

                ListView {

                    model: searchEngines.modelByName[searchEngine.searchersNames[index]]
                    visible: searchEngines.modelByName[searchEngine.searchersNames[index]]

                    delegate: RowLayout {

                        anchors.left: parent.left
                        anchors.right: parent.right

                        Label {
                            Layout.fillHeight: true
                            Layout.fillWidth: true

                            text: title
                            elide: Label.ElideRight
                        }

                        Button {
                            text: qsTr("GO")

                            onClicked: {
                                Qt.openUrlExternally(name);
                            }
                        }
                    }
                }
            }

            ListView {

                model: searchEngines.rangingList

                delegate: RowLayout {

                    anchors.left: parent.left
                    anchors.right: parent.right

                    Label {
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        text: title
                        elide: Label.ElideRight
                    }

                    Button {
                        text: qsTr("GO")

                        onClicked: {
                            Qt.openUrlExternally(name);
                        }
                    }
                }
            }
        }



        footer: TabBar {
            id: bar

            width: parent.width
            position: TabBar.Footer
            currentIndex: swipeView.currentIndex

            Repeater {
                model: searchEngine.searchersNames

                TabButton {
                    text: qsTr(searchEngine.searchersNames[index])
                }
            }

            TabButton {
                text: qsTr("Ranging list")
            }
        }
    }
}
