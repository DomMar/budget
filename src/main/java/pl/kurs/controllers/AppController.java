package pl.kurs.controllers;

import javafx.fxml.FXML;

public class AppController {

    private MainController mainController;

    @FXML
    public void beckMenu (){
        mainController.loadMenuScreen();

    }

    public void setMainController(MainController mainController)
    {
        this.mainController = mainController;
    }
}
