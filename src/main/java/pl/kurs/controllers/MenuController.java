package pl.kurs.controllers;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.layout.Pane;

import java.io.IOException;

public class MenuController {

    //umieszczmy instację klasy mainController w tej klasie
    private MainController mainController;

    @FXML
    public void openApplication(){
        //w mainscreenie ładujemy appscreena
        FXMLLoader loader = new FXMLLoader(this.getClass().getResource("/fxml/appScreen.fxml"));
       //nasz appscreen jest pane
        Pane pane= null;
        try {
             pane = loader.load();
        } catch (IOException e) {
            e.printStackTrace();
        }
        AppController appController = loader.getController();
        appController.setMainController(mainController);
        mainController.setScreen(pane);

    }

    @FXML
    public void openOption(){
        FXMLLoader loader = new FXMLLoader(this.getClass().getResource("/fxml/OptionsScreen.fxml"));
        Pane pane = null;
        try {
            pane = loader.load();
        } catch (IOException e) {
            e.printStackTrace();
        }
        OptionsController optionsController = loader.getController();
        optionsController.setMainController(mainController);
        mainController.setScreen(pane);
    }

    @FXML
    public void exit(){
        Platform.exit();
    }

    public void setMainController(MainController mainController) {
        this.mainController = mainController;
    }
}



