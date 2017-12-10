package hebrewNER.hmm;

import java.util.List;

import vohmm.corpus.*;
import vohmm.util.*;

/**
 * The Hmm name finder tags token using the statistical model read from a file.<br>
 * The search for the best tag sequence is done by Viterbi search.
 */
public class HmmNameFinder{
	
	private HmmModel hmm;
	private NodeIndexer ni;
	private HmmContextGenerator cg;
	private int[] bestSequence;
	private String[] bestSequenceTags;
	
	// parameters use by the viterbi search
	private double[] prevProbs, curProbs;
	private int[][] nodePointers;
	private int numOfNode;
	
	public HmmNameFinder(String modelFile){
		hmm = HmmModel.readFromFile(modelFile);
		ni = new NodeIndexer();
		cg=new HmmContextGenerator();
	}
	
	public HmmNameFinder(){
		this("models/NER.hmm.model");
	}
	
	/**
  	 * tag a sentence using a Viterbi search on the HMM.
   	 * @param toks   the array of sentence tokens 
   	 * @param posAnal   the part of speech analysis
   	 * @return The array of corresponding named entity tags
   	 */
	public String[] tag(String[] toks, Sentence posAnal){
		bestSequence = viterbi(cg.getContext(toks),posAnal);
		bestSequenceTags = sequenceTags(bestSequence);
		return bestSequenceTags;
	}
	
	/**
  	 * Preforms a Viterbi search on a sentence using its conetext an pos analysis
   	 * @param context   the array of context for the sentece tokens
   	 * @param posAnal   the part of speech analysis
   	 * @return The array ints representing the nodes of the best sequence
   	 */
	public int[] viterbi(String[] context, Sentence posAnal){
		
		numOfNode=ni.getNumOfNodes();
		int searchLen=context.length;
		nodePointers=new int[searchLen][numOfNode];
		for(int i=0;i<searchLen;i++)
			for(int j=0;j<numOfNode;j++)
				nodePointers[i][j]=-1;
		
		prevProbs=new double[numOfNode+1];
		prevProbs[ni.getSOSIndex()]=1;	
		
		Anal wAnal;
		String wpos;
		int[] possibleNodes;
		int maxNode;
		for(int i=0;i<searchLen;i++){
			curProbs=new double[numOfNode];
			wAnal = posAnal.getToken(i).getSelectedAnal(); 
			wpos = Long.toString(wAnal.getTag().getBitmask() & Bitmask.BASEFORM_POS);
			for(int j=1;j<numOfNode;j++){
				//the transition to another node is possible only if it maches the pos
				//tag of this token
				if(ni.isPosNode(wpos,j)){
					maxNode=getMax(j);
					nodePointers[i][j]=maxNode;
					curProbs[j]=hmm.getEmissionP(j,context[i])
							*prevProbs[maxNode]
							*hmm.getTransitionP(maxNode,j);
				}
				else{
					curProbs[j]=0;
				}				
			}
			prevProbs=curProbs;			
		}
		
		return getMaxPath();
	}
	
	//find the node with the maximum probability so far
	private int getMax(int toNode){
		double max=0;
		int maxNode=-1;
		double val;
		boolean start=true;
		for(int i=0;i<numOfNode;i++){
			val=prevProbs[i]*hmm.getTransitionP(i,toNode);
			if((start || val>=max) && ni.validSequence(i,toNode)){
				max=val;
				maxNode=i;
				start=false;
			}
		}
		return maxNode;
	}
	
	//find the maximum probability path in the matrix created by the search
	private int[] getMaxPath(){
		int searchLen=nodePointers.length;
		int[] nodePath=new int[searchLen];
		int lastNode=getMax(ni.getEOSIndex());
		for (int i=searchLen-1;i>=0;i--){
			nodePath[i]=lastNode;
			lastNode=nodePointers[i][lastNode];
		}
		return nodePath;
	}
			
	//finds the sequence of tags created by the path with the maximum probability 
	private String[] sequenceTags(int[] seq){
		String[] tags=new String[seq.length];
		for(int i=0;i<tags.length;i++){
			tags[i]=ni.getNodeTag(seq[i]);
		}			
		return tags;
	}
	
}