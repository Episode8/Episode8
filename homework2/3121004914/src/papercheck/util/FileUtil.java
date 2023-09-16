package src.papercheck.util;


import src.papercheck.pojo.Paper;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.text.NumberFormat;


public final class FileUtil {

    /**
     * 读取论文内容
     * @param filePath 目标文件地址
     * @return 论文模型
     */
    public static Paper readFromFile(String filePath){
        Paper paper = new Paper();
        BufferedReader reader = null;
        String tempString;
        StringBuilder builder = new StringBuilder();
        try {
            reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), StandardCharsets.UTF_8));
            // 一次读入一行，直到读入null为文件结束
            while ((tempString = reader.readLine()) != null) {
                builder.append(tempString.trim());
            }
        } catch (UnsupportedEncodingException e) {
            System.out.println("目前不支持该编码格式，请更换其他编码格式！");
            e.printStackTrace();
        } catch (IOException e) {
            if (e instanceof FileNotFoundException){
                System.out.println("找不到该文件，请检查文件路径是否正确！");
            }else {
                System.out.println("读取文件异常!");
            }
            e.printStackTrace();
        } finally {
            if (reader != null){
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        tempString = builder.toString();
        paper.setSentence(tempString.replaceAll("。", "")
                .replaceAll("，", "")
                .replaceAll(",", ""));
        return paper;
    }

    /**
     * 将结果写入文件中
     * @param path 输出文件地址
     * @param result 输出的内容
     */
    public static void writeInFile(String path, String result){
        File file = createFileIfNotExist(path);
        BufferedWriter out = null;
        try {
            out = new BufferedWriter(new OutputStreamWriter(
                    new FileOutputStream(file, true), StandardCharsets.UTF_8));
            out.write(result);
            out.flush();
        } catch (IOException e) {
            System.out.println("文件写入异常！");
            e.printStackTrace();
        }finally {
            try {
                if(out != null){
                    out.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        System.out.println(result);
    }

    /**
     * 确保目标文件存在
     * @param path 目标文件目录
     * @return 文件模型
     */
    public static File createFileIfNotExist(String path){
        File file = null;
        String fileDir = path.substring(0, path.lastIndexOf(File.separatorChar));
        File dirs = new File(fileDir);
        if (!dirs.exists() || !dirs.isDirectory()) {
            if (!dirs.mkdirs()){
                try {
                    throw new Exception("无法创建文件夹，请检查文件路径是否正确！");
                } catch (Exception e) {
                    System.out.println(e.getMessage());
                    e.printStackTrace();
                    return null;
                }
            }
        }
        file = new File(path);
        if (!file.exists() || !file.isFile()){
            try {
                if (!file.createNewFile()){
                    throw new Exception("无法创建文件，请检查文件路径是否正确！");
                }
            } catch (Exception e) {
                System.out.println(e.getMessage());
                e.printStackTrace();
                return null;
            }
        }
        return file;
    }

    /**
     * 转换重复率
     * @param rate 重复率的浮点数
     * @return 重复率的字符串
     */
    public static String getPercentFormat(double rate){
        NumberFormat nf = java.text.NumberFormat.getPercentInstance();
        // 小数点后保留几位
        nf.setMinimumFractionDigits(2);
        return nf.format(rate);
    }
}