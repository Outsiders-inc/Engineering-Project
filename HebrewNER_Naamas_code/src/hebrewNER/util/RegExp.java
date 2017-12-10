package hebrewNER.util;

import java.io.*;
import java.util.StringTokenizer;

/**
 * A class that identifies hebrew long regular expressions(1-5 words)<br>
 * Contains binary methods to identify organization, location, date, time, money,
 * and percent expressions. <br>
 * Creates only one instance of this class.<br>
 * Takes use of a hebrew dictionary.
 */
public class RegExp{
	
	private static RegExp re;	
	private Dictionary dictionary,nounsMinus1;
	
	private RegExp(){
		dictionary = Dictionary.getInstance("lists/Dictionary.txt");	
		nounsMinus1 = Dictionary.getInstance("lists/nouns-1.txt");
	}
	
   /**
   * @return the one instance of this class
   */
	public static RegExp getInstance(){
		if(re!=null) return re;
		re = new RegExp();
		return re;		
	}
	
   /**
   * Identify organization expression
   * @param ppw - prev prev word, pw - prev word, w - current word, nw - next word
   * nnw - next next word  
   * @return "#t" if true and "#f" if false.
   */
	public String isOrg(String ppw,String pw,String w,String nw,String nnw, String wf){
    	if(isOrg(ppw,pw,w) || isOrg(pw,w,nw)|| isOrg(w,nw,nnw) 
    		 || wf.equals("loazi")
    		 || (dictionary.getDictionary(ppw,pw,w,nw, nnw).equals("ORG"))
 			 || dictionary.getDictionary(w, "ORG"))
 			 return "#t";
 		return "#f";
 	}
 	
	private boolean isOrg(String w,String nw,String nnw){
		if( nounsMinus1.getDictionary(w,"ORG")
			&& (dictionary.getDictionary(nw, "LOC")
			   || dictionary.getDictionary(nw+" "+nnw, "LOC")
			   || dictionary.getDictionary(nw, "PER")))
			return true;
		return false;
	}
	
   /**
   * Identify location expression
   * @param ppw - prev prev word, pw - prev word, w - current word, nw - next word
   * nnw - next next word  
   * @return "#t" if true and "#f" if false.
   */
	public String isLoc(String ppw,String pw,String w,String nw,String nnw){
    	if( isLoc(pw,w) || isLoc(w,nw)
    		 || (dictionary.getDictionary(ppw,pw,w,nw, nnw).equals("LOC"))
 			 || dictionary.getDictionary(w, "LOC"))
 			 return "#t";
 		return "#f";
 	}
 	
	private boolean isLoc(String w,String nw){
		if(nounsMinus1.getDictionary(w,"LOC") 
			&& dictionary.getDictionary(nw, "PER"))
			   return true;
		return false;
	}
	
   /**
   * Identify date expression
   * @param toks - an array of strings representing a sentence, 
   * wIndex - index of the current word
   * @return "#t" if true and "#f" if false.
   */
	public String isDate(String[] toks, int wIndex){
		String w=toks[wIndex];
		String ppw=null,pw=null,nw=null,nnw=null;
		if(wIndex-1>=0) pw=toks[wIndex-1];
		if(wIndex-2>=0) ppw=toks[wIndex-2];
		if(wIndex+1<toks.length) nw=toks[wIndex+1];
		if(wIndex+2<toks.length) nnw=toks[wIndex+2];
		if(	quarter(toks,wIndex)
				|| (ppw!=null && (numMonthYear(ppw,pw,w)|| dictionary.getDictionary(ppw+" "+pw+" "+w,"DATE")))
				|| (pw!=null && nw!=null && (numMonthYear(pw,w,nw) || dictionary.getDictionary(pw+" "+w+" "+nw,"DATE")))
				|| (nw!=null && nnw!=null && (numMonthYear(w,nw,nnw) ||dictionary.getDictionary(w+" "+nw+" "+nnw,"DATE")))
				|| (pw!=null && (numMonth(pw,w) || dictionary.getDictionary(pw+" "+w,"DATE")))
				|| (nw!=null && (numMonth(w,nw) || dictionary.getDictionary(w+" "+nw,"DATE")))
				|| date(w)	|| isDigitInRange(w,1800,2200,0)
				|| dictionary.getDictionary(w,"DATE"))
				return "#t";
		else return "#f";
				
	}
	
	private boolean numMonthYear(String ppw, String pw,String w){
		return ( (isDigitInRange(ppw,0,32,0) || dictionary.getDictionary(ppw,"NUM"))
				 && dictionary.getDictionary(pw,"DATE")
				 && isDigitInRange(w,1800,2200,0));
	}
	
	private boolean numMonth(String pw,String w){
		return ( (isDigitInRange(pw,0,32,0) || dictionary.getDictionary(pw,"NUM"))
				 && dictionary.getDictionary(w,"DATE"));
	}
	
	private boolean date(String w){
		if (w.length()< 6 || w.length()> 10)
    		return false;
    	String[] s= w.split("\\.");
    	if (s.length==1) s= w.split("-");
    	if (s.length !=3)
    		return false;
    	return(isDigitInRange(s[0],0,32)
    		   && isDigitInRange(s[1],0,13)
    		   && ((s[2].length()==2 && isDigitInRange(s[2],-1,100))
    		   		||(s[2].length()==4 && isDigitInRange(s[2],1800,2200))));
    }
    
   private boolean quarter(String[] toks, int wIndex){
		int i=Math.max(0,wIndex-4);
		boolean q=false;
		for (;i<=wIndex && i+2<toks.length ;i++){
			String exp=toks[i]+" "+toks[i+1]+" "+toks[i+2];
			if(dictionary.getDictionary(exp,"QUARTER")){
				q=true;
				break;
			}
		}
		if(q&& (i+3<toks.length && isDigitInRange(toks[i+3],1800,2200) && wIndex<=i+3)
				|| i+4<toks.length && isDigitInRange(toks[i+4],1800,2200) && wIndex<=i+4)
				return true;
		return false;
	}
	
   /**
   * Identify expression inside inverted commas 
   * @param toks - an array of strings representing a sentence, 
   * wIndex - index of the current word
   * @return "#t" if true and "#f" if false.
   */		
	public String inCommas(String[] toks, int wIndex){
		int start=Math.max(0,wIndex-5);
		int end=Math.min(toks.length,wIndex+6);
		boolean in=false;
		char c;
		String tok;
		for(int i=start;i<wIndex;i++){
			tok=toks[i];
			if(tok.length()>0&&tok.charAt(0)==34)
				in=true;
		}
		tok=toks[wIndex];
		if(tok.length()>1 && tok.charAt(0)==34)
			in=true;
		if(in){
			if(tok.length()>1&&tok.charAt(tok.length()-1)==34)
				return "#t";
			for(int i=wIndex+1;i<end;i++){
				tok=toks[i];
				if(tok.length()>0&&tok.charAt(tok.length()-1)==34)
					return "#t";
				}
		}
		return "#f";		
	}
	
   /**
   * Identify precent expression
   * @param pw - prev word, w - current word, nw - next word
   * @return "#t" if true and "#f" if false.
   */	
    public String isPercent(String pw,String w, String nw){
    	if(isPercent(w,0) || isPercent(pw,w) || isPercent(w,nw))
    		return "#t" ;
    	return "#f" ;
    }
    
    private boolean isPercent(String w, int prefRemoved){
    	if (dictionary.getDictionary(w,"PERCENT"))
    		return true;
    	if(TokenInfo.wordFeature(w).equals("np")
    		&& isDigitInRange(w.substring(0,w.length()-1),0,101))
    		return true;
    	if(TokenInfo.wordFeature(w).equals("pn")
    		&& isDigitInRange(w.substring(1),0,101))
    		return true;
    	if(prefRemoved<3 && w.length()>1)
    		return isPercent(w.substring(1),prefRemoved+1);   	
    	return false;
    }
    	    
    private boolean isPercent(String pw,String w){
    	if(pw!=null && w!=null){
    		if ((isDigitInRange(pw,0,101,0)
    			|| dictionary.getDictionary(pw, "NUM"))
    			&& (TokenInfo.wordFeature(w).equals("per")
    			||dictionary.getDictionary(w,"PERCENT")))
    			return true;
     		if ((isDigitInRange(w,0,101,0)
    			|| dictionary.getDictionary(w, "NUM"))
    			&& (TokenInfo.wordFeature(pw).equals("per")
    			||dictionary.getDictionary(pw,"PERCENT")))
    			return true;
    	}
    	return false;
    }
    
   /**
   * Identify time expression
   * @param pw - prev word, w - current word, nw - next word
   * @return "#t" if true and "#f" if false.
   */
    public String isTime(String pw,String w,String nw){
    	if(isTime(pw, w) || isTime(w,nw) || isTime(w))
    			 return "#t";
		return "#f" ;
    }
    
    private boolean isTime(String w){
    	if(time(w)
    		|| (w.length()>1&&time(w.substring(1)))
    		|| (w.length()>2&&time(w.substring(2))))
    			return true;
		return false ;
    }
    
    private boolean isTime(String w,String nw){
    	if(nounsMinus1.getDictionary(w,"TIME") && isTime(w))
    		return true;
		return false;
    }
    
    private boolean time(String word){
    	if (word.length()< 4 || word.length()> 5)
    		return false;
    	if (word.length()==5 && word.indexOf(":") != 2 && word.indexOf(".") != 2 )
    		return false;
    	String hours = word.substring(0,2);
    	if(!isDigitInRange(hours,-1,25))
    		return false;
    	String mins;
    	if(word.length()==4)
    		mins = word.substring(2,4);
    	else mins = word.substring(3);
    	if(!isDigitInRange(mins,-1,60))
    		return false;
    	return true;
    }
    
   /**
   * Identify money expression
   * @param ppw - prev prev word, pw - prev word, w - current word, nw - next word
   * nnw - next next word  
   * @return "#t" if true and "#f" if false.
   */
    public String isMoney(String ppw,String pw,String w,String nw,String nnw){
    	if(isMoney(pw,w) || isMoney(w,nw) || isMoney(ppw,pw,w)
 			 || isMoney(pw,w,nw)|| isMoney(w,nw,nnw) 
 			 || dictionary.getDictionary(w, "MONEY"))
 			 return "#t";
 		return "#f";
 	}
    
    private boolean isMoney(String pw,String w){
    	if(pw!=null && w!=null && isNumber(pw)
    	 	&& dictionary.getDictionary(w, "MONEY"))
    	 	return true;
    	if(pw!=null && w!=null && isNumber(w)
    	 	&& dictionary.getDictionary(pw, "MONEY"))
    	 	return true;
    	if (dictionary.getDictionary(pw+" "+w,"MONEY"))
    		return true;
    	return false;     	
    }
    
    private boolean isMoney(String pw,String w,String nw){
    	if(pw!=null && nw!=null && isNumber(pw)){
    		if (dictionary.getDictionary(w,"NUM")
    			&& dictionary.getDictionary(nw,"MONEY"))
    			return true;
    		if (dictionary.getDictionary(w+" "+nw,"MONEY"))
    			return true;
    	}
    	return false;
    }
     
	private boolean isNumber(String w){
		if(dictionary.getDictionary(w,"NUM"))
			return true;
		return isDigit(w,0);
	}
	
	private boolean isDigit(String w,int prefRemoved){	
		if(prefRemoved < 3){
			try{
				double num = Double.parseDouble(w.replaceAll(",",""));
				return true;
    		}
    		catch (NumberFormatException nfe){
    			return (w.length() > 1 && isDigit(w.substring(1),prefRemoved+1));
    		}
    	}
    	return false;
    }  
    
    private boolean isDigitInRange(String w,int from,int to){
     	try {
    		double num = Double.parseDouble(w=w.replaceAll(",",""));
    		if (num > from && num < to) 
    			return true;
    	}
    	catch (NumberFormatException nfe){
    		return false;
    	}
    	return false;
     }
     
     private boolean isDigitInRange(String w,int from,int to,int prefRemoved){
     	if(prefRemoved < 3){
     		try {
     			double num = Double.parseDouble(w=w.replaceAll(",",""));
     			if (num > from && num < to) 
     				return true;
     		}
     		catch (NumberFormatException nfe){
     			return (w.length() > 1 && isDigit(w.substring(1),prefRemoved+1));
     		}
    	}
    	return false;
     }
     
  }
    
 