package Test;

import org.junit.Test;
import src.papercheck.Main;

import src.papercheck.pojo.Paper;
import src.papercheck.util.CalculatorUtil;
import src.papercheck.util.FileUtil;

import java.io.File;

import static src.papercheck.util.FileUtil.getPercentFormat;


public class test {

    @Test
    public void testMain(){
        long before = System.currentTimeMillis();
        String originalText1 = "D:\\Work\\大二\\软件工程\\homework2\\homework\\Test\\resources\\orig.txt";
        String modifiedText2 = "D:\\Work\\大二\\软件工程\\homework2\\homework\\Test\\resources\\orig.txt";
        String modifiedText3 = "D:\\Work\\大二\\软件工程\\homework2\\homework\\Test\\resources\\orig2.txt";
        Paper originalText = FileUtil.readFromFile(originalText1);
        Paper modifiedText = FileUtil.readFromFile(modifiedText2);
        try {
            Thread.sleep(5000);
            System.out.println(34234);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        CalculatorUtil.calculate(originalText, modifiedText);
        double repetitionRate = modifiedText.getRepetitionRate();
        java.io.File file = FileUtil.createFileIfNotExist(modifiedText3);
        if (file == null){
            return;
        }
        String result = "===================================\n" +
                "总字数：" + modifiedText.getSum() + "\n" +
                "重复字数：" + modifiedText.getRepetition() + "\n" +
                "重复率：" + getPercentFormat(modifiedText.getRepetitionRate()) + "\n" +
                "时间用了" + (double)(System.currentTimeMillis() - before)/1000 + "秒\n" +
                "===================================";
        FileUtil.writeInFile(modifiedText3, result);
    }


    @Test
    public void testMain2(){
        Main.main(new String[]{"1.txt","D:\\Work\\大二\\软件工程\\homework2\\homework\\Test\\resources\\orig_0.8_add.txt","D:\\1.txt"});
    }

    @Test
    public void test(){
        System.out.println(File.separatorChar);
        System.out.println(File.pathSeparatorChar);
    }
}