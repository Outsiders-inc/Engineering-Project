package hebrewNER.hmm;

import java.util.Hashtable;

/**
 * Class for indexing the nodes of the HMM. Each node is a product of a part of speech
 * tag and a named entity tag. special nodes are start and end of sentence.<br>
 * Contains methods for encoding and decoding nodes. 
 */
public class NodeIndexer{
	
	//the named entity tag set
	public final static String[] tags={"I_PERS","B_PERS","I_LOC","B_LOC","I_ORG","B_ORG",
					"I_MONEY","B_MONEY","I_TIME","B_TIME","I_PERCENT","B_PERCENT",
					"I_DATE","B_DATE","O"};
					
	//the part of speech represented by its long coding
	public final static String[] pos={"393216","983040","1114112","524288","786432",
										"196608","655360","720896","262144","851968",
										"458752","131072","65536","589824"};
	private Hashtable stringToIndex;
	private Hashtable indexToString;
	private int numOfNodes,EOS,SOS;
	
	
	/**
   	* Creates a new NodeIndexer instance by indexing the nodes
   	*/
	public NodeIndexer(){
		stringToIndex = new Hashtable();
		indexToString = new Hashtable();
		numOfNodes=0;
		
		//create start of sentece node
		Integer curInt=new Integer(numOfNodes);
		SOS=numOfNodes;
		stringToIndex.put("SOS",curInt);
		indexToString.put(curInt,"SOS");
		
		//create end of sentece node
		numOfNodes++;
		curInt=new Integer(numOfNodes);
		EOS=numOfNodes;	
		stringToIndex.put("EOS",curInt);
		indexToString.put(curInt,"EOS");
		
		//creating the product nodes
		for (int i=0;i<pos.length;i++){
			for (int j=0;j<tags.length;j++){
					numOfNodes++;
					curInt = new Integer(numOfNodes);
					stringToIndex.put(tags[j]+" "+pos[i],curInt);
					indexToString.put(curInt,tags[j]+" "+pos[i]);
			}
		}
		numOfNodes++;
	}
	
	public int getNumOfNodes(){ return numOfNodes;}
	
	public int getNumOfTags(){ return tags.length;}

	/**
  	 * @return The index of the start of sentence node
   	 */
	public int  getSOSIndex(){ return SOS;}
	
	/**
  	 * @return The index of the end of sentence node
   	 */
	public int  getEOSIndex(){ return EOS;}
	
	/**
  	 * @param tag   the named entity tag
  	 * @param wpos   the part of speech tag in its long representation
   	 * @return The index of the node created by their product
   	 */
	public int  getIndex(String tag,String wpos){
		Integer node=(Integer)stringToIndex.get(tag+" "+wpos);
		if (node==null) node=(Integer)stringToIndex.get(tag+" 0");
		if(node!=null) return node.intValue();
		return -1;
	}
	
	/**
  	 * @param index   node index
   	 * @return The named entity tag of this node
   	 */
	public String getNodeTag(int index){
		String tag=((String)indexToString.get(new Integer(index))).split(" ")[0];
		return tag;
	}
	
	/**
  	 * @param index   node index
   	 * @return The pos tag of this node in its long representation
   	 */
	public String getNodePos(int index){
		String n=(String)indexToString.get(new Integer(index));
		if(!n.equals("EOS")&&!n.equals("SOS"))
			return n.split(" ")[1];
		return "";
	}
	
	/**
  	 * Checks if this node pos tag is wpos
   	 */
	public boolean isPosNode(String wpos, int node){
		if(node==getSOSIndex() && wpos==null) return true;
		return getNodePos(node).equals(wpos);
	}
	
	/**
  	 * Chacks if fromNode and toNode are a valid sequence
   	 */
	public boolean validSequence(int fromNode,int toNode){
		String toTag=getNodeTag(toNode);
		if(toTag.startsWith("B_")){
			if (fromNode==getSOSIndex()) return false;
			toTag=toTag.substring(2);
			String fromTag=getNodeTag(fromNode);
			if (fromTag.equals("O")) return false;
			if (!fromTag.substring(2).equals(toTag)) return false;
		}
		return true;
	}
}

 			