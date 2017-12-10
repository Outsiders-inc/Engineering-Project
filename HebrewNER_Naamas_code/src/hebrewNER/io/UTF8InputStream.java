package hebrewNER.io;
 
 import java.util.List;
 import java.util.ArrayList;
 import java.io.*;
 
 /** 
  * Stream for processing trainig file.<br>
  * Process hebrew UTF8 files of the format:
  * word per line, the first column or each line is the token and the second column
  * is the NE tag.<br>
  * The sentences are separated by an empty line.<br>
  * Each document begins with "--DOCSTART-- O"<br>
  * The stream returns a sentance at a time;
 */
 public class UTF8InputStream{

	public static final String DOCSTART="--DOCSTART-- O";
 	private BufferedReader reader; 			
 	private String curLine;
   	private List tags, tokens;
   
 	/**
   	* Creates a new <code>SDContextGenerator</code> instance from the the file named 
   	* by fileName 
   	*/
 	public UTF8InputStream(String fileName){
 		try {
 			reader=new BufferedReader(
 				new InputStreamReader(new FileInputStream(fileName), "UTF8"));
			curLine=reader.readLine();
			while(curLine.equals("")) 
				curLine=reader.readLine();
		}
 		catch(IOException e){
 			e.printStackTrace();
			System.exit(2);
		}		
		if (!hasNextFile()){
			System.out.println("UTF8InputStream: can't initiate, wrong file format");
			System.exit(1);
		}
		
 	}
 	
 	public boolean hasNextFile(){
  		return curLine!=null && curLine.startsWith(DOCSTART);
    }
    
    /**
   	* has next sentence 
   	*/
    public boolean hasNextSent(){
    	return curLine!=null && !curLine.startsWith(DOCSTART);
    }
    
    /**
   	* reads the next sentence, separates tags and tokens to separate lists.
   	* @return a List of Strings of the current tokens
   	*/
    public List nextSentTokens(){
    	tokens = new ArrayList();
    	tags= new ArrayList();
 		String tag;
 		String[] l;
 		try{
    		if(curLine.startsWith(DOCSTART)){
    			//remove empty line
    			 reader.readLine();
    			 curLine=reader.readLine();
    		}
    		for(;curLine!=null && !curLine.equals(""); curLine=reader.readLine()) {
    			l=curLine.split(" ");
    			tokens.add(l[0]);
    			tag=l[1];
    			//remove misc tags
    			if(tag.length()>6 && tag.substring(2,6).equals("MISC"))
    				tag="O";
    			tags.add(tag);    			
    		}
    		curLine=reader.readLine();
    	}
    	catch(IOException e){
    		e.printStackTrace();
    		System.exit(2);
    	}    	
    	return tokens;
    }
    
    /**
   	* @return a string of the current sentence
   	*/
    public String tokensAsString(){
    	String sentence="";
    	for(int i=0;i<tokens.size();i++){
    		sentence+=(String)tokens.get(i)+" ";
    	}
    	return sentence;
    }
	
	/**
   	* @return a List of Strings of the current tags
   	*/
    public List nextSentTags(){
    	 return tags;
	 }	
}