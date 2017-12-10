package hebrewNER.hmm;

import java.util.Hashtable;

/**
 * A class for training HMM from a corpus in one training file. Calculates the
 * transition and emission probabilitis.<br>
 * The HMM nodes are defined by the NodeIndexer and the vocabulary is the set
 * of contexts created by the context generator using the event stream.<br>
 * The HMM created is saved in a file.
 */
public class TrainHmm{
	
	private  Hashtable[] emission;
	private int[] emissionTotal;
	private int[][] transitions;
	private int[] transitionsTotal;
	private Hashtable vocabulary;
	private NodeIndexer ni;
	private int numOfNodes;
	private	HmmEventStream es;
	
	public TrainHmm(String inputFile){
		ni = new NodeIndexer();
		numOfNodes=ni.getNumOfNodes();
		transitions = new int[numOfNodes][numOfNodes];
		transitionsTotal=new int[numOfNodes];
		vocabulary=new Hashtable();
		emissionTotal=new int[numOfNodes];
		emission=new Hashtable[numOfNodes];
		for (int i=0;i<emission.length;i++)
			emission[i]=new Hashtable();
		es= new HmmEventStream(inputFile);				
	}
	
	/**
  	 * train HMM using the event stream.
   	 */
	public HmmModel train(){
		Event event1,event2;
		int node1,node2;
		do{
			event1=null;
			node1=ni.getSOSIndex();
			while(event1==null || es.hasNext()){
				event2=es.nextEvent();
				node2=ni.getIndex(event2.tag,event2.pos);
				putW(event2.context,node2);
				transitions[node1][node2]++;
				transitionsTotal[node1]++;
				event1=event2;
				node1=node2;
			}
			event2=null;
			node2=ni.getEOSIndex();
			transitions[node1][node2]++;
			transitionsTotal[node1]++;
		}while(es.hasNextSent());
		return new HmmModel(transitions, transitionsTotal, emission,
							 emissionTotal,vocabulary.size(),numOfNodes);
	}
	
	//puts a symbol in the vocabulary
	private void putW(String context,int nodeIndex){
		if(!emission[nodeIndex].containsKey(context)){
			int[] val={0};
			emission[nodeIndex].put(context,val);
		}
		((int [])emission[nodeIndex].get(context))[0]++;
		emissionTotal[nodeIndex]++;
		vocabulary.put(context,"");		
	}
	
	/**
  	 * main method for training HMM and saving it into a file
   	 * Usage: TrainHmm training_file model_file
   	 */
	public static void main(String[] args){
		if (args.length !=2) {
			System.out.println("Usage: TrainHmm training_file model_file");
			System.exit(1);
		}
		TrainHmm t = new TrainHmm(args[0]);
		HmmModel hmm = t.train();		
		hmm.writeToFile(args[1]);
	}
	
	
}