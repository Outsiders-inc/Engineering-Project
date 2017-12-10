package hebrewNER.baseline;

import java.util.HashMap;
import java.util.List;
import java.io.*;

import hebrewNER.io.*;


 /** 
  * A class for training the baseline model and saving it to file.
  * The main class is used for training.
 */
public class TrainBaseline{
	
	private HashMap dict;
	
	public TrainBaseline(){
		dict = new HashMap();
	}
	
	/**
	 * Creates a lexicon of all the named entity expressions which appear in 
	 * the training file.
   	 * @param trainFile the name of the training file
   	 */
	public void train(String trainFile){
		UTF8InputStream input = new UTF8InputStream(trainFile);
		List tokens,tags;
		String curExp="",curTag="";
		while(input.hasNextFile()){
			do{
				tokens=input.nextSentTokens();
				tags=input.nextSentTags();
				for(int i=0;i<tokens.size();i++){
					String tag=(String)tags.get(i);
					if(tag.equals("O")){
						if(!curExp.equals("")&&!curTag.equals("")){
							dict.put(curTag+" "+curExp,"");
							curExp="";
							curTag="";
						}
					}
					else if(tag.equals("I_"+curTag)){
						//inside an expression
						curExp+=" "+(String)tokens.get(i);
					}
					else{
						//a new expression
						if(!curExp.equals("")&&!curTag.equals(""))
							dict.put(curTag+" "+curExp,"");
						curExp=(String)tokens.get(i);
						curTag=tag.substring(2);
					}					
				}
			}while(input.hasNextSent());
		}
	}
	
	/**
  	 * Saves the model as a hebrew UTF8 file.<br>
  	 * The file created contains the lexicon created by the train method.
  	 * An expression pre line.
   	 * @param fileName  the name of the model file.
   	 */
	public void saveModelToFile(String fileName){
		System.out.println("writing list to: "+fileName);
		try{
			BufferedWriter	out = new BufferedWriter(new OutputStreamWriter(
									new FileOutputStream(fileName), "UTF8"));
			Object [] keys=dict.keySet().toArray();
			for(int i=0;i<keys.length;i++){
				out.write((String)keys[i]+"\n");
			}
			out.close();
		}
		catch(IOException e){
   			e.printStackTrace();
  	 		System.exit(2);
   		}
   	}
	
	/**
  	 * Main method for training
   	* Usage: TrainBaseline training_file model_file
   	*/
	public static void main(String[] args){
		if (args.length !=2) {
			System.out.println("Usage: TrainBaseline training_file model_file");
			System.exit(1);
		}
		TrainBaseline t= new TrainBaseline();
		t.train(args[0]);
		t.saveModelToFile(args[1]);
	}
	
}