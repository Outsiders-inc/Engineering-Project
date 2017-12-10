package hebrewNER.maxent;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import opennlp.maxent.*;
import hebrewNER.io.*;
import gnu.trove.*;

import vohmm.corpus.*;
import vohmm.application.Tagger2;

/**
 * This event stream is used by the train class for training maxent model from
 * a file containig the training set.<br>
 * The stream returns one Event at a time. The context of an event is generated by
 * MaxEntContextGenerator.
 */
public class MaxEntEventStream implements EventStream {
	
	private UTF8InputStream data;
	private String[] toks,outcomes;
	private MaxEntContextGenerator cg;
	private Map prevTags;
	private int curSentIter;
	private Tagger2 posTagger;
	private Sentence posAnal;
	
	/**
   	 * Creates a new MaxEntEventStream instance
   	 * @param fileName   the name of the training file
   	 */
	public MaxEntEventStream(String fileName) {
		data = new UTF8InputStream(fileName);
		posTagger = new Tagger2();
		cg = new MaxEntContextGenerator(posTagger);
		prevTags = new Hashtable();
		loadSentence();
	}
	
	//read the next sentence from the file and spliting its data to the corresponding arrays
	private void loadSentence(){
		if(data.hasNextFile()){
			prevTags.clear();
		}
		else if(data.hasNextSent()){
			for(int i=0;i<outcomes.length;i++)
				prevTags.put(toks[i],outcomes[i]);
		}
		List temp = data.nextSentTokens();
		toks = (String[]) temp.toArray(new String[temp.size()]);
		temp = data.nextSentTags();		
		outcomes = (String[]) temp.toArray(new String[temp.size()]);
		posAnal = posTagger.tagSentence(data.tokensAsString());
		curSentIter = 0;
	}
		
	/**
  	 * @return The next event in the training file.
   	 */	
	public Event nextEvent() {
		if (curSentIter == toks.length){
			loadSentence();
		}
		Event next = new Event((String) outcomes[curSentIter]
						,cg.getContext(curSentIter, toks, outcomes, posAnal, prevTags));
		curSentIter++;
		return next;
	}
	
	/**
  	 * has next event
   	 */
	public boolean hasNext(){
		return (curSentIter < toks.length || data.hasNextSent() || data.hasNextFile());
	}
	
}