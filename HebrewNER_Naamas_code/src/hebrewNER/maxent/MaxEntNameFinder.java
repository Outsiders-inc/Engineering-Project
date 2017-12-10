package hebrewNER.maxent;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.Arrays;

import opennlp.maxent.MaxentModel;
import opennlp.maxent.io.SuffixSensitiveGISModelReader;
import opennlp.tools.util.*;

import vohmm.corpus.*;
import vohmm.application.Tagger2;


 /**
 * The MaxEnt name finder tags token using the statistical model read from a file.<br>
 * The search for the best tag sequence is done by beam search.
 */
public class MaxEntNameFinder {
	
	private MaxentModel maxent;
	private MaxEntContextGenerator cg;
	private Sequence bestSequence;
	private int beamSize;
	private BeamSearch beam;
	private Map prevTags;
	
	
	/**
  	 * Creates a new MaxEntEventStream instance. Loads the maxent model from a known file
  	 * Initiate a beam search with beam size 10.
   	 * @param posTagger   part of speech tagger
   	 */	
	public MaxEntNameFinder(Tagger2 posTagger) {
		try{
			maxent = new SuffixSensitiveGISModelReader
						(new File("models/NER.maxent.model")).getModel();
				 
		}
		catch(IOException e){
			e.printStackTrace();
			System.exit(2);
		}
		cg = new MaxEntContextGenerator(posTagger);
		beamSize = 10;
		beam = new NameBeamSearch(beamSize, cg, maxent);
		prevTags = new Hashtable();
	}
	
	/**
  	 * Creates a new MaxEntEventStream instance
  	 * Initiate a beam search with beam size 10.
   	 * @param mod   maxent model
   	 * @param posTagger   part of speech tagger
   	 */	
	public MaxEntNameFinder(MaxentModel mod, Tagger2 posTagger) {
		this(mod, posTagger, 10);
	}
	
	/**
  	 * Creates a new MaxEntEventStream instance
   	 * @param mod   maxent model
   	 * @param posTagger   part of speech tagger 
   	 * @param beamSize   size of the beam used by the beam search. 
   	 */	
	public MaxEntNameFinder(MaxentModel mod, Tagger2 posTagger, int beamSize) {
		maxent = mod;
		cg = new MaxEntContextGenerator(posTagger);
		this.beamSize = beamSize;
		beam = new NameBeamSearch(beamSize, cg, mod);
		prevTags = new Hashtable();
	}
	
	/**
  	 * tag a sentence using a beam search on the maxent model.
   	 * @param toks   the array of sentence tokens 
   	 * @param posAnal   the part of speech analysis
   	 * @return The array of corresponding named entity tags
   	 */
	public String[] tag(String[] toks, Sentence posAnal) {
		List tokens = Arrays.asList(toks);
		bestSequence = beam.bestSequence(tokens, new Object[] {posAnal, prevTags});
		List c = bestSequence.getOutcomes();
		String[] tags = (String[]) c.toArray(new String[c.size()]);
		for(int i=0;i<tags.length;i++)
			prevTags.put(toks[i],tags[i]);
		return tags;
	}
	
	/**
  	 * @return The probabilites of the best sequence of tags.
   	 */	
	public double[] probs(){
		return bestSequence.getProbs();
	}
	
	
	private class NameBeamSearch extends BeamSearch {
		
		public NameBeamSearch(int size, MaxEntContextGenerator cg, MaxentModel model) {
			super(size, cg, model);
		}
		
		protected boolean validSequence(int i, List sequence, Sequence s, String outcome) {
			if(outcome.startsWith("B_")){
				String curTag=outcome.substring(2);
				List tags = s.getOutcomes();
				int li = tags.size() - 1;
				if (li == -1) return false;
				if (((String) tags.get(li)).equals("O")) return false;
				if (!((String) tags.get(li)).substring(2).equals(curTag)) return false;
			}
			return true;
		}
	}
}