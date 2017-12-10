package hebrewNER.hmm;

import java.util.*;
import java.io.*;


/**
 * Holds a Hmm. Holds its emission and transition probabilities. <br>
 * Creation of a new model can be done from its constructor of from file. 
 * A model can also be saved in a file for future use.
 */
public class HmmModel{
	
	private Hashtable[] emission;
	private int[] emissionTotal;
	private int [][] transitions;
	private int [] transitionsTotal;
	//to avoid zero probabilities, cause by a small corpus, use Laplace correction
	private double vCorrection,nCorrection; 
	private int vocabularySize,numOfNodes;
		
	
	public HmmModel(int[][] transitions, int[] transitionsTotal,Hashtable[] emission,
					int[] emissionTotal,int vocabularySize,int numOfNodes){
		this.emission=emission;
		this.emissionTotal=emissionTotal;
		this.transitions=transitions;
		this.transitionsTotal=transitionsTotal;
		this.vocabularySize=vocabularySize;
		this.numOfNodes=numOfNodes;
		vCorrection=(double)1/vocabularySize;
		nCorrection=(double)1/numOfNodes;
	}
	
	/**
  	 * @return The number of nodes for this HMM
   	 */
	public double getNumOfNodes(){
		return numOfNodes;
	}
	
	/**
  	 * Get transition probability from nodeFrom to nodeTo.
   	 * @return The probability or the Laplace correction if zero.
   	 */
	public double getTransitionP(int nodeFrom, int nodeTo){
		if(transitions[nodeFrom][nodeTo]!=0)
			return 
			((double)transitions[nodeFrom][nodeTo]/transitionsTotal[nodeFrom])
				+nCorrection;
		return nCorrection;
	}
	
	/**
  	 * Get emission probability of context from node
   	 * @return The probability or the Laplace correction if zero.
   	 */
	public double getEmissionP(int node,String context){
		if(emission[node].containsKey(context)){
			return 
			(double)((int[])emission[node].get(context))[0]/emissionTotal[node]
				+vCorrection;
		}
		return vCorrection;
	}
	
	/**
  	 * Save the model to file.
   	 * @param modelFile   the name of the model file
   	 */
	public void writeToFile(String modelFile){
		try {
			System.out.println("writing HMM model to file: "+modelFile);
			FileWriter fi = new FileWriter(modelFile);
			PrintWriter os = new PrintWriter(fi);
			os.println("HMM MODEL");
			
			os.println(vocabularySize);
			os.println(numOfNodes);
			
			for (int i=0;i<transitionsTotal.length;i++){
				os.print(transitionsTotal[i]+" ");
			}
			os.print("\n");
			
			
			for (int i=0;i<transitions.length;i++)
				for (int j=0;j<transitions[0].length;j++){
					os.print(transitions[i][j]+" ");
				}
			os.print("\n");
			
			for (int i=0;i<emissionTotal.length;i++){
				os.print(emissionTotal[i]+" ");
			}
			os.print("\n");
			
			Set keys;
			Iterator iter;
			String keyTemp;
			int[] valTemp;
			for (int i=0;i<emission.length;i++){
				keys= emission[i].keySet();
				iter=keys.iterator() ;
				while(iter.hasNext()){
					keyTemp=(String)iter.next();
					valTemp=(int [])emission[i].get(keyTemp);
					os.print(keyTemp+" "+valTemp[0]+" ");
				}
				os.print("\n");
			}
								
			os.close();
			fi.close();
		}
		catch(IOException e) {
			System.out.print("Error while writing: " + e);
		}
	}
	
	/**
  	 * Load a model from file
   	 * @param modelFile   the name of the model file
   	 * @return a new instance of HmmModel
   	 */
	public static HmmModel readFromFile(String modelFile){
		int vSize=0,numOfN=0;
		int[][] trans=null;
		int[] eTotal=null,tTotal=null;
		Hashtable[] e=null;
		try {
			FileReader fr = new FileReader(modelFile);
			BufferedReader is = new BufferedReader(fr);
			StringTokenizer st;
			
			if(!is.readLine().equals("HMM MODEL")){
				System.out.print("Error: wrong file format");
				System.exit(2);
			}
			
			st=new StringTokenizer(is.readLine());
			vSize=Integer.parseInt(st.nextToken());
			
			st=new StringTokenizer(is.readLine());
			numOfN=Integer.parseInt(st.nextToken());
			
			tTotal=new int[numOfN];
			st=new StringTokenizer(is.readLine());
			for (int i=0;i<tTotal.length;i++){
				tTotal[i]=Integer.parseInt(st.nextToken());
			}
						
			trans=new int[numOfN][numOfN];
			st=new StringTokenizer(is.readLine());
			for (int i=0;i<numOfN;i++)
				for (int j=0;j<numOfN;j++){
					trans[i][j]=Integer.parseInt(st.nextToken());
				}
				
			eTotal=new int[numOfN];
			st=new StringTokenizer(is.readLine());
			for (int i=0;i<numOfN;i++){
				eTotal[i]=Integer.parseInt(st.nextToken());
			}
			
			e=new Hashtable[numOfN];
			String keyTemp;
			int valTemp;
			for (int i=0;i<numOfN;i++)
				e[i]=new Hashtable();
			for (int i=0;i<numOfN;i++){
				st=new StringTokenizer(is.readLine());
				while(st.hasMoreTokens()){
					keyTemp=st.nextToken();
					valTemp=Integer.parseInt(st.nextToken());
					int [] val={valTemp};
					e[i].put(keyTemp,val);
				}
			}			
			is.close();
		}
		
		catch(IOException exp) {
			System.out.print("Error: while reading " + exp);
			System.exit(2);
		}
		
		return new HmmModel(trans,tTotal,e,eTotal,vSize,numOfN);
	}
	
}
	