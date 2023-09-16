package src.papercheck.component;
public class EnterNullException extends Exception {
    public EnterNullException(){
    }
    public EnterNullException(String message){
        super(message);
    }
}