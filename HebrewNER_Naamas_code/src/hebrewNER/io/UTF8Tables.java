package hebrewNER.io;

import java.util.Hashtable;

/**
 * Class used for converting UTF8 characters to tatiq characters.
 */
 
public class UTF8Tables{

	/*
	 * hebrew2tatiq table maps Hebrew characters UTF-8
	 * into Latin characters
	 */
	 
	 public static Hashtable hebrew2tatiq = new Hashtable(30);
	 static {
	 	hebrew2tatiq.put(new Character((char)1488),new Character('A'));
	 	hebrew2tatiq.put(new Character((char)1489),new Character('B'));
	 	hebrew2tatiq.put(new Character((char)1490),new Character('G'));
	 	hebrew2tatiq.put(new Character((char)1491),new Character('D'));
	 	hebrew2tatiq.put(new Character((char)1492),new Character('H'));
	 	hebrew2tatiq.put(new Character((char)1493),new Character('W'));
	 	hebrew2tatiq.put(new Character((char)1494),new Character('Z'));
	 	hebrew2tatiq.put(new Character((char)1495),new Character('X'));
	 	hebrew2tatiq.put(new Character((char)1496),new Character('@'));
	 	hebrew2tatiq.put(new Character((char)1497),new Character('I'));
	 	hebrew2tatiq.put(new Character((char)1498),new Character('K'));
	 	hebrew2tatiq.put(new Character((char)1499),new Character('K'));
	 	hebrew2tatiq.put(new Character((char)1500),new Character('L'));
	 	hebrew2tatiq.put(new Character((char)1501),new Character('M'));
	 	hebrew2tatiq.put(new Character((char)1502),new Character('M'));
	 	hebrew2tatiq.put(new Character((char)1503),new Character('N'));
	 	hebrew2tatiq.put(new Character((char)1504),new Character('N'));
	 	hebrew2tatiq.put(new Character((char)1505),new Character('S'));
	 	hebrew2tatiq.put(new Character((char)1506),new Character('&'));
	 	hebrew2tatiq.put(new Character((char)1507),new Character('P'));
	 	hebrew2tatiq.put(new Character((char)1508),new Character('P'));
	 	hebrew2tatiq.put(new Character((char)1509),new Character('C'));
    	hebrew2tatiq.put(new Character((char)1510),new Character('C'));
   		hebrew2tatiq.put(new Character((char)1511),new Character('Q'));
    	hebrew2tatiq.put(new Character((char)1512),new Character('R'));
    	hebrew2tatiq.put(new Character((char)1513),new Character('$'));
    	hebrew2tatiq.put(new Character((char)1514),new Character('T'));
  	}
  	
  	/**
  	 * tatiq2hebrew table maps Latin characters into
  	 * Hebrew characters
  	 **/
  	 public static Hashtable tatiq2hebrew = new Hashtable(30);
  	 static {
  	 	tatiq2hebrew.put(new Character('A'),new Character((char)1488));
    	tatiq2hebrew.put(new Character('B'),new Character((char)1489));
    	tatiq2hebrew.put(new Character('G'),new Character((char)1490));
    	tatiq2hebrew.put(new Character('D'),new Character((char)1491));
    	tatiq2hebrew.put(new Character('H'),new Character((char)1492));
    	tatiq2hebrew.put(new Character('W'),new Character((char)1493));
    	tatiq2hebrew.put(new Character('Z'),new Character((char)1494));
    	tatiq2hebrew.put(new Character('X'),new Character((char)1495));
    	tatiq2hebrew.put(new Character('@'),new Character((char)1496));
    	tatiq2hebrew.put(new Character('I'),new Character((char)1497));
    	tatiq2hebrew.put(new Character('K'),new Character((char)1498));
    	tatiq2hebrew.put(new Character('K'),new Character((char)1499));
    	tatiq2hebrew.put(new Character('L'),new Character((char)1500));
    	tatiq2hebrew.put(new Character('M'),new Character((char)1501));
    	tatiq2hebrew.put(new Character('M'),new Character((char)1502));
    	tatiq2hebrew.put(new Character('N'),new Character((char)1503));
    	tatiq2hebrew.put(new Character('N'),new Character((char)1504));
    	tatiq2hebrew.put(new Character('S'),new Character((char)1505));
    	tatiq2hebrew.put(new Character('&'),new Character((char)1506));
    	tatiq2hebrew.put(new Character('P'),new Character((char)1507));
    	tatiq2hebrew.put(new Character('P'),new Character((char)1508));
    	tatiq2hebrew.put(new Character('C'),new Character((char)1509));
    	tatiq2hebrew.put(new Character('C'),new Character((char)1510));
    	tatiq2hebrew.put(new Character('Q'),new Character((char)1511));
    	tatiq2hebrew.put(new Character('R'),new Character((char)1512));
    	tatiq2hebrew.put(new Character('$'),new Character((char)1513));
    	tatiq2hebrew.put(new Character('T'),new Character((char)1514));
  	}
  	
  	/**
   * Converts UTF8 hebrew string to tatiq string using the tables encoding.
   * @param input string to convert  
   * @return the converted string
   */
  	public static String hebrew2tatiq(String input){
  		String converted="";
  		Character  c;
  		for(int i=0;i<input.length();i++){
  			c=(Character)hebrew2tatiq.get(new Character(input.charAt(i)));
  			if(c==null) converted+=input.charAt(i);
  			else converted+=c.charValue();
  		}
  		return converted;
  	}
  }
