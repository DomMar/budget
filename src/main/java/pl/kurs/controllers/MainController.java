package pl.kurs.controllers;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;

import java.io.IOException;

public class MainController {



    @FXML
    private StackPane mainStackPane;

    @FXML
    public void initialize(){
        loadMenuScreen();

    }

    public void loadMenuScreen() {
        //w tej metodzie załadujemy sobie nowe okno
        FXMLLoader loader = new FXMLLoader(this.getClass().getResource("/fxml/MenuScreen.fxml"));
        //nasz screen jest Painem
        Pane pane = null;
        try {
            pane = loader.load();
        } catch (IOException e) {
            e.printStackTrace();
        }

        //wyciągamy referencje naszego kontrolera
        MenuController menuController = loader.getController();
        //do mainControlera przekazujemy instancję tej klasy
        menuController.setMainController(this);

        //to własnie w stackpane umieszczamy menuscreen
        //do stackpane wrzucamy manupane
        setScreen(pane);
    }

    public void setScreen(Pane pane){
        //czescimy zeby nam sie nie nakłądaly eleemnty okiena na siebie
        mainStackPane.getChildren().clear();
        mainStackPane.getChildren().add(pane);
    }
}
