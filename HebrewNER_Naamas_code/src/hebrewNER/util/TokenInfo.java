package hebrewNER.util;

import java.util.Vector;
import java.util.regex.Pattern;
import java.io.*;

import hebrewNER.io.UTF8Tables;

/**
 * a class that hold patterns to give token information
 */
 
public class TokenInfo{
	
	private static Vector feats;
	private static Vector featsNames;
	private static boolean  loaded=false;
	
	
	/**
   * Identify token information, for example: oneDigits, floatingPointNumber,
   * contains comma, contains number.
   * @param word
   * @return a string representing the information found
   */
	public static String wordFeature(String word) {
		if(isLoazi(word)) return "loazi";
		if(!loaded) initPatterns();
		String tatiq = UTF8Tables.hebrew2tatiq(word);
		for(int i=0; i<feats.size();i++){
			if(((Pattern)(feats.elementAt(i))).matcher(tatiq).find())
				return (String)featsNames.elementAt(i);
		}
		return "#f";
	}
	
	
	private static void initPatterns() {
		feats = new Vector();
  		featsNames = new Vector();
  	    
    	feats.add(Pattern.compile("^[0-9]$"));                         		//oneDigits
    	featsNames.add("od");
    	feats.add(Pattern.compile("^[0-9][0-9]$"));                         //twoDigits
    	featsNames.add("td");
    	feats.add(Pattern.compile("^[0-9][0-9][0-9][0-9]$"));               //fourDigits
    	featsNames.add("fd");
    	feats.add(Pattern.compile("^[0-2][0-9]\\:[0-5][0-9]$"));            //hour
    	featsNames.add("time");
    	feats.add(Pattern.compile("^[0-9]+$"));                             //naturalNumber
		featsNames.add("nn");
		feats.add(Pattern.compile("^[0-9]+\\.[0-9]+$"));                    //floatingPointNumber
		featsNames.add("fpn");
		feats.add(Pattern.compile("^[0-9]+\\.?[0-9]*\\%$"));                //numberPrecent
    	featsNames.add("np");
    	feats.add(Pattern.compile("^\\%[0-9]+\\.?[0-9]*$"));                //numberPrecent
    	featsNames.add("pn");
    	feats.add(Pattern.compile("^\\%$"));                				//Precent
    	featsNames.add("per");
    	feats.add(Pattern.compile("^([0-9]+\\.[0-9]*)+$"));                 //numberDot
		featsNames.add("nd");
		feats.add(Pattern.compile("^[0-9]+\\/[0-9]+\\/[0-9]+$"));           //digitSlash
		featsNames.add("ds");
		feats.add(Pattern.compile("^[0-9]+\\-[0-9]+\\-[0-9]+$"));          //digitDash
		featsNames.add("dd");
		feats.add(Pattern.compile("-"));                                    //containsHyphens
    	featsNames.add("ch");
    	feats.add(Pattern.compile("/"));                                    //containsBackslash
    	featsNames.add("cbs");
    	feats.add(Pattern.compile(","));                                    //containsComma
    	featsNames.add("cc");
    	feats.add(Pattern.compile("\\."));                                  //containsPeriod
    	featsNames.add("p");
    	feats.add(Pattern.compile("[0-9]"));                                //containsNumber
    	featsNames.add("cn");
	         
    	feats.trimToSize();
	    featsNames.trimToSize();
    	loaded = true;
  	}
  	
  	private static boolean isLoazi(String word){
  		word = word.toUpperCase();
  		char[] cc = word.toCharArray();
  		for(int i=0;i<cc.length;i++)
  			if (cc[i] >= 65 && cc[i] <= 90)
  				return true;
  		return false;
  	}
  	
  }