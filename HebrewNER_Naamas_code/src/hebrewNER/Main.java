package hebrewNER;

import java.io.*;

import hebrewNER.maxent.*;
import hebrewNER.hmm.*;
import hebrewNER.baseline.*;
import hebrewNER.sentenceDetect.*;
import hebrewNER.io.*;

import vohmm.corpus.*;
import vohmm.application.Tagger2;

/**
 * Command line utility recognizes named entities
 * in hebrew UTF8 text. 
 */
 
public class Main{
	
   
   /**
   * main method<br>
   * Usage: java Main source_file<br>
   * where source_file is hebrew UTF8 file<br>
   * Output tagged file in the same directory
   * as the source file with ending ".ner"
   */
   
	public static void main(String[] args)throws IOException{
		
		if(args.length!=1){
			System.err.println("Usage: java Main source_file");
			System.exit(0);
		}
		
		String fileName=args[0];
		File f = new File(fileName);
		if (!f.exists() || !f.isFile()){
			System.err.println("Source file doesn't exist or not a file");
			System.exit(0);
		}
		
		String input="";		
		System.out.println("Reading Text from "+fileName);
		BufferedReader reader=new BufferedReader(
 				new InputStreamReader(new FileInputStream(fileName), "UTF8"));
		for(String line=reader.readLine();line!=null;line=reader.readLine()) 
			input+=line+"\n";
				
		System.out.println("Detecting Sentences");
		String[] sentences = new SentenceDetector().sentDetect(input);
		
		System.out.println("Initiating Part of Speech Tagger...");
		PrintStream console = System.out;
		PrintStream stdout = new PrintStream(new BufferedOutputStream(new FileOutputStream("ner_log")));
		System.setOut(stdout);
		Tagger2 posTagger = new Tagger2();
		stdout.close(); 
    	System.setOut(console);
    	
		MaxEntNameFinder me = new MaxEntNameFinder(posTagger);
		HmmNameFinder hmm = new HmmNameFinder();
		BaselineNameFinder base = new BaselineNameFinder();
		
		String[] tokens, maxEntTags, hmmTags, baselineTags, tags;
		Sentence posAnal;
		String sentenceTokens, output="";
		
		System.out.println("Tokenizing and Tagging Sentences...");
		for(int i=0;i<sentences.length;i++){
			sentenceTokens = Tokenizer.tokenize(sentences[i]);
			posAnal=posTagger.tagSentence(sentenceTokens);
			tokens = sentenceTokens.split(" ");
			maxEntTags = me.tag(tokens, posAnal);
			hmmTags = hmm.tag(tokens, posAnal);
			baselineTags = base.tag(tokens);
			tags = merge(maxEntTags, hmmTags, baselineTags);
			for(int j=0;j<tokens.length;j++){
				output+=tokens[j]+"\t"+tags[j]+"\n";
			}
				output+="\n";
		}
		
		//print output to file
		String outputFileName = fileName;
		int dot = outputFileName.lastIndexOf(".");
		if (dot == -1)  outputFileName = outputFileName + ".ner";
		else outputFileName = outputFileName.substring(0,dot) + ".ner";
		System.out.println("Saving Tagged Data to "+outputFileName);
		BufferedWriter out = new BufferedWriter(new OutputStreamWriter(
 								new FileOutputStream(outputFileName), "UTF8"));
 		out.write(output);
 		out.close();
 		
  	 	File toRemove= new File("Tagger2_log");
		toRemove.delete();
		toRemove= new File("ner_log");
		toRemove.delete();
	}
	
	// merges the 3 tagging outputs by empirical conditions
	private static String[] merge(String[] maxEntTags,String[] hmmTags,String[] baselineTags){
		String[] tags=new String[maxEntTags.length];
		String meTag, hmmTag, baseTag;
		for (int i=0;i<maxEntTags.length;i++){
			meTag=maxEntTags[i];
			hmmTag=hmmTags[i];
			baseTag=baselineTags[i];
			if(!meTag.equals("O") && meTag.substring(2).equals("DATE")){
				if(!hmmTag.equals("O")&&hmmTag.substring(2).equals("DATE"))
					tags[i]=meTag;
				else if(!baseTag.equals("O")&&baseTag.substring(2).equals("TIME"))
					tags[i]=baseTag;
			}
			tags[i]=meTag;
			if(meTag.equals("O")){
				if( !hmmTag.equals("O")
					 && (hmmTag.substring(2).equals("LOC") 
						|| hmmTag.substring(2).equals("ORG")
						|| hmmTag.substring(2).equals("MONEY")))
						tags[i]=hmmTag;
				else if (!baseTag.equals("O") && baseTag.substring(2).equals("LOC"))
						tags[i]=baseTag;
			}			
			if(tags[i].equals("O") && !hmmTag.equals("O")
				&& !hmmTag.substring(2).equals("PERS")
				&& hmmTag.equals(baseTag))
					tags[i]=hmmTag;
		}
		return tags;
	}
}