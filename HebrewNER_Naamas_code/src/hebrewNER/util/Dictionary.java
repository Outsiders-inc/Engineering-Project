package hebrewNER.util;

import java.util.Hashtable;
import java.util.StringTokenizer;
import java.io.*;

/** 
 * Dictionary holds several volumes of a dictionary.<br>
 * each volume is held as a hash table and has only one instance.
 */
 
public class Dictionary{
	
	private static Hashtable volumes = new Hashtable();;
	private Hashtable dictionary;
	private String dictName;
	private final String[] tags={"PERS","LOC","ORG", "DATE","MONEY","TIME", "PERCENT"};
	
	private Dictionary(String dictName){
		this.dictName=dictName;
		dictionary = new Hashtable();
		loadDict();
	}
	
   /**
   * @return the instance of the volume represented by dictName
   */
	public static Dictionary getInstance(String dictName){
		if(volumes.containsKey(dictName))
			return (Dictionary)volumes.get(dictName);
		Dictionary d=new Dictionary(dictName);
		volumes.put(dictName,d);
		return d;		
	}
	
	//loads a volume from a UTF8 text file.
	private void loadDict(){
	 	try{
	 		BufferedReader br=new BufferedReader(
	 			new InputStreamReader(new FileInputStream(dictName), "UTF8"));
	 		StringTokenizer st;
	 		String  line= null;
	 		String category,word;
	 		while((line = br.readLine()) != null){
	 				st = new StringTokenizer(line);
	 				word ="";
	 				category = st.nextToken();
	 				while(st.hasMoreTokens())
	 					word+=st.nextToken()+" ";
		 			word=word.trim();
		 			dictionary.put(word+" "+category,"#t");
		 	}
	 	}
	 	catch (Exception e){
	 		e.printStackTrace();
	 		System.exit(2);
	 		return;
	 	}
	 }
	 
   /**
   * looks for the dictionary entry of the longest expression in a window of 
   * +-2 around current word.
   * @param ppw - prev prev word, pw - prev word, w - current word, nw - next word
   * nnw - next next word  
   * @return a string representing the dictionary entry, "#f" if not found
   */	
	public String getDictionary(String ppw,String pw,String w,String nw,String nnw){
		String ans;
		ans=getDictionary(ppw+" "+pw+" "+w);
		if(!ans.equals("#f")) return ans; 
		ans=getDictionary(pw+" "+w+" "+nw);
		if(!ans.equals("#f")) return ans; 
		ans=getDictionary(w+" "+nw+" "+nnw);
		if(!ans.equals("#f")) return ans; 
		ans=getDictionary(pw+" "+w);
		if(!ans.equals("#f")) return ans; 
		ans=getDictionary(w+" "+nw);
		if(!ans.equals("#f")) return ans; 
		ans=getDictionary(w);
		return ans;
	}
	
   /**
   * looks for the dictionary entry of a single word
   * @param word current word, nw - next word
   * @return a string representing the dictionary entry, "#f" if not found
   */	
	public String getDictionary(String word){
		for(int i=0;i<tags.length;i++){
			if (getDictionary(word+" "+tags[i],0))
				return tags[i];
		}
		
		return "#f";
	}
	
	/**
   * checks if dictionary entry of a word if tag.
   */
	public boolean getDictionary(String word, String tag){
		if (getDictionary(word+" "+tag,0))
			return true;
		return false;
	}
	
	//looks for the dictionary entry of the word without its prefixes
	private boolean getDictionary(String word,int prefRemoved){
		if (dictionary.containsKey(word))
			return true;
		else if (prefRemoved == 0 && word.length()>=3){
			char ch = word.charAt(0);
			if (ch ==1492 /*h*/ ||ch == 1493 /* vav */||ch == 1513 /* shin */ )
				return getDictionary(word.substring(1,word.length()),1);
			else if (ch == 1489 /* bet */ || ch == 1499 /* kaf */ || 
						ch == 1500 /* lamed */ || ch == 1502 /* mem */  )
				return getDictionary(word.substring(1,word.length()),2);
		}
		else if (prefRemoved == 1 && word.length()>=3){
			char ch = word.charAt(0);
			if (ch ==1492 /*h*/ ||ch == 1489 /* bet */ || ch == 1499 /* kaf */ || 
					ch == 1500 /* lamed */ || ch == 1502 /* mem */  )
				return getDictionary(word.substring(1,word.length()),2);
		}
		return false;
	}
	
	/////////////REMOVE////////////////////
	public int getDictPrefix(String word,int prefRemoved){
		if (dictionary.containsKey(word))
			return prefRemoved;
		else if (prefRemoved == 0 && word.length()>=3){
			char ch = word.charAt(0);
			if (ch ==1492 /*h*/ ||ch == 1493 /* vav */||ch == 1513 /* shin */ )
				return getDictPrefix(word.substring(1,word.length()),1);
			else if (ch == 1489 /* bet */ || ch == 1499 /* kaf */ || 
						ch == 1500 /* lamed */ || ch == 1502 /* mem */  )
				return getDictPrefix(word.substring(1,word.length()),2);
		}
		else if (prefRemoved == 1 && word.length()>=3){
			char ch = word.charAt(0);
			if (ch ==1492 /*h*/ ||ch == 1489 /* bet */ || ch == 1499 /* kaf */ || 
					ch == 1500 /* lamed */ || ch == 1502 /* mem */  )
				return getDictPrefix(word.substring(1,word.length()),2);
		}
		return -1;
	}
	
}
 	
