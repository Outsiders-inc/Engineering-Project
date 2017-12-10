package hebrewNER.sentenceDetect;

import opennlp.maxent.*;
import opennlp.maxent.io.*;

import opennlp.maxent.IntegerPool;
import opennlp.tools.util.Pair;

import java.io.*;
import java.util.List;
import java.util.ArrayList;


/**
 * SentenceDetector uses a Maximum Entropy model to find the sentence boundaries in
 * a text. 
 */ 

public class SentenceDetector {
	private MaxentModel model;
	private final ContextGenerator cgen;
	private final EndOfSentenceScanner scanner;
	// a pool of read-only java.lang.Integer objects in the range 0..100
  	private static final IntegerPool INT_POOL = new IntegerPool(100);
	// the index of the "true" outcome in the model
	private final int _trueIndex;
	private List sentProbs;
	
	/**
  	* @param name The MaxentModel file which this SentenceDetector will use to
   	* evaluate end-of-sentence decisions.
   	*/
   	public SentenceDetector(String name){
   		try{
   			model = new SuffixSensitiveGISModelReader(new File(name)).getModel();
   		}
   		catch(IOException e){
   			e.printStackTrace();
   			System.exit(2);
   		}
   		cgen = new SDContextGenerator(EndOfSentenceScanner.eosCharacters);
   		scanner = new EndOfSentenceScanner();
   		sentProbs = new ArrayList(50);
   		_trueIndex = model.getIndex("T");
   	}
   	
   	public SentenceDetector(){
   		this("models/SD.maxent.model");
   	}
   	
   	/**
   	* Detect sentences in a String.
   	* @param s  The string to be processed.
   	* @return   A string array containing individual sentences as elements.
   	*/
   	public String[] sentDetect(String s) {
   		int[] starts = sentPosDetect(s);
    	String[] sents = new String[starts.length];
    	if(starts.length!=0){
	    	sents[0] = s.substring(0,starts[0]);
    		int si = 1;
       		for (; si < starts.length; si++) {
	    		sents[si] = s.substring(starts[si - 1], starts[si]);
    		}
    		if(starts[si-1]!=s.length()){
    			String[] sents1=new String[sents.length+1]	;
    			for(int i=0;i<sents.length;i++)
	    			sents1[i]=sents[i];
    			sents1[sents.length]=s.substring(starts[si-1]);
    			sents=sents1;
    		}
    	}
    	else{
    		sents = new String[]{s};
    	}
  		return sents;
  	}
  	
  	private int getFirstWS(String s, int pos) {
  		while (pos < s.length() && !Character.isWhitespace(s.charAt(pos)))
  			pos++;
  		return pos;
  	}

  	private int getFirstNonWS(String s, int pos) {
    	while (pos < s.length() && Character.isWhitespace(s.charAt(pos)))
      		pos++;
    	return pos;
  	}

  	/**
   	* Detect the position of the first words of sentences in a String.
   	* @param s  The string to be processed.
   	* @return   A integer array containing the positions of the end index of
   	*          every sentence
   	*           
   	*/
  	public int[] sentPosDetect(String s) {
  		double sentProb = 1;
    	sentProbs.clear();
    	StringBuffer sb = new StringBuffer(s);
    	List enders = scanner.getPositions(s);
    	List positions = new ArrayList(enders.size());
	    
	    for (int i = 0, end = enders.size(), index = 0; i < end; i++) {
	    	Integer candidate = (Integer) enders.get(i);
      		int cint = candidate.intValue();
		    // skip over the leading parts of contiguous delimiters
		    if (((i + 1) < end) && (((Integer) enders.get(i + 1)).intValue() == (cint + 1))) {
		    	continue;
		    }
		    Pair pair = new Pair(sb, candidate);
		    String[] c=cgen.getContext(pair);
            double[] probs = model.eval(cgen.getContext(pair));
		    String bestOutcome = model.getBestOutcome(probs);
		    sentProb *= probs[model.getIndex(bestOutcome)];
		    if (bestOutcome.equals("T")) {
		    	if (index != cint) {
		    		positions.add(INT_POOL.get(getFirstNonWS(s, cint + 1)));
		    		sentProbs.add(new Double(probs[model.getIndex(bestOutcome)]));
		    	}
		    	index = cint + 1;
		    }
		 }
		 int[] sentPositions = new int[positions.size()];
		 for (int i = 0; i < sentPositions.length; i++) {
		 	sentPositions[i] = ((Integer) positions.get(i)).intValue();
		 }
		 return sentPositions;
	}
}
