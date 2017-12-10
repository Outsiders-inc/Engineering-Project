package hebrewNER.baseline;

import java.util.List;

import hebrewNER.util.*;


/** 
 * The BaselineNameFinder tags tokens by regular expression and lexicon created from
 * training file.<br>
 * Regular expression identify date, time, momey and precent expressions.<br>
 * A token gets its tag by its lexicon entry.
 */
public class BaselineNameFinder{
	
	private Dictionary trainDict;
	private RegExp regExp;
	
	/**
   	* Creates a new <code>BaselineNameFinder</code> instance 
   	* @param dictName the name of the baseline model file.
   	*/
	public BaselineNameFinder(String dictName){
		trainDict = Dictionary.getInstance(dictName);
		regExp= RegExp.getInstance();
	}
	
	public BaselineNameFinder(){
		this("models/NER.baseline.model");
	}
	
	/**
  	 * Tag a sentence.
   	 * @param toks   the array of sentence tokens 
   	 * @return The array of corresponding tags as given by the baseline model
   	 */
	public String[] tag(String[] toks){
		String[] tags=new String[toks.length];
		String ppw, pw, w, nw, nnw, predTag;
		
		for(int i=0;i<toks.length;i++){
			w = toks[i];
			if (i - 2 >= 0) ppw = toks[i - 2];
 			else ppw=null;
 			if (i > 0){
 				pw = toks[i - 1];
 				predTag=tags[i-1];
 			}
 			else{
 				pw=null;
 				predTag=null;
 			}
 			if (i + 1 < toks.length) nw = toks[i + 1];
 			else nw=null;
 			if (i + 2 < toks.length) nnw = toks[i + 2];
 			else nnw=null;
 			
 			//check for regular expressions
 			if(regExp.isPercent(pw,w,nw).equals("#t"))
 				tags[i]="I_PERCENT";
 			else if(regExp.isMoney(ppw,pw,w,nw,nnw).equals("#t"))
 				tags[i]="I_MONEY";
 			else if(regExp.isTime(pw,w,nw).equals("#t"))
 				tags[i]="I_TIME";
 			else if(regExp.isDate(toks,i).equals("#t"))
 				tags[i]="I_DATE";
 			else{
 				//check dictionary
 				tags[i]=getTag(predTag,ppw,pw,w,nw,nnw);
 			}
 		}
 		return tags;
		
	}
	
	private String getTag(String predTag, String ppw,String pw,String w,String nw,String nnw){
		String ans;
		ans=trainDict.getDictionary(ppw+" "+pw+" "+w);
		if(!ans.equals("#f")) return "I_"+ans; 
		ans=trainDict.getDictionary(pw+" "+w+" "+nw);
		if(!ans.equals("#f")) return "I_"+ans; 
		ans=trainDict.getDictionary(w+" "+nw+" "+nnw);
		if(!ans.equals("#f")) return cont(predTag,ans);
		ans=trainDict.getDictionary(pw+" "+w);
		if(!ans.equals("#f")) return "I_"+ans; 
		ans=trainDict.getDictionary(w+" "+nw);
		if(!ans.equals("#f")) return cont(predTag,ans);
		ans=trainDict.getDictionary(w);
		if(!ans.equals("#f")) return cont(predTag,ans);
		return "O";
	}
	
	private String cont(String predTag, String curTag){
		if(predTag!=null){
			if(predTag.length()>2)
				predTag=predTag.substring(2);
			if (predTag.equals(curTag)) return "B_"+curTag;			
		}
		return "I_"+curTag;
	}
}