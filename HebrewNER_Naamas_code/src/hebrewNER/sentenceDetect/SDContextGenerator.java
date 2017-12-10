package hebrewNER.sentenceDetect;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;

import opennlp.tools.util.Pair;
import opennlp.maxent.ContextGenerator;


/**
 * Generate event contexts for maxent decisions for sentence detection.
 */

public class SDContextGenerator implements ContextGenerator {
	
	private StringBuffer buf = new StringBuffer();
  	private List collectFeats = new ArrayList();
  	private char[] eosCharacters;

  	/**
   	* Creates a new <code>SDContextGenerator</code> instance 
   	*/
  	public SDContextGenerator(char[] eosCharacters) {
	    this.eosCharacters = eosCharacters;
  	}
  	
  	/**
   	* Builds up the list of features, anchored around a position within the
   	* StringBuffer. 
   	*/
  	public String[] getContext(Object o) {
  		/** String preceeding the eos character in the eos token. */
  		String prefix;
    	/** Space delimited token preceeding token containing eos character. */
    	String previous;
    	/** String following the eos character in the eos token. */
    	String suffix;
    	/** Space delimited token following token containsing eos character. */
    	String next;
    	Object first = ((Pair) o).a;
    	/** Character offset of eos character in */
    	int position = ((Integer) ((Pair) o).b).intValue();

	    if (first instanceof String[]) {
	    	String[] $_ = (String[]) first;
	    	previous = $_[0];
      		String current = $_[1];
      		prefix = current.substring(0, position);
      		suffix = current.substring(position + 1);
      		if (suffix.startsWith(" "))
        		collectFeats.add("sn");
      		if (prefix.endsWith(" "))
        		collectFeats.add("pn");
      		collectFeats.add("eos=" + current.charAt(position));
      		next = $_[2];
    	}
    	else {
    		//compute previous, next, prefix and suffix Strings and space previous, space next features and eos features. 
    		StringBuffer sb = (StringBuffer) ((Pair) o).a;
    		int lastIndex = sb.length() - 1;
      		// compute space previous and space next features.
      		if (position > 0 && sb.charAt(position - 1) == ' ')
          		collectFeats.add("sp");
      		if ((position < lastIndex && sb.charAt(position + 1) == ' ')||position == lastIndex)
          		collectFeats.add("sn");
      		collectFeats.add("eos=" + sb.charAt(position));
      		int prefixStart = previousSpaceIndex(sb, position);

      		int c = position;
      		{
      		///assign prefix, stop if you run into a period though otherwise stop at space
      		while (--c > prefixStart) {
      			for (int eci = 0, ecl = eosCharacters.length; eci < ecl; eci++) {
      				if (sb.charAt(c) == eosCharacters[eci]) {
      					prefixStart = c;
      					c++; // this gets us out of while loop.
      					break;
      				}
      			}
      		}
      		prefix = sb.substring(prefixStart, position).trim();
      		}
      		int prevStart = previousSpaceIndex(sb, prefixStart);
      		previous = sb.substring(prevStart, prefixStart).trim();
      		int suffixEnd = nextSpaceIndex(sb, position, lastIndex);
      		{
      			c = position;
      			while (++c < suffixEnd) {
      				for (int eci = 0, ecl = eosCharacters.length; eci < ecl; eci++) {
      					if (sb.charAt(c) == eosCharacters[eci]) {
      						suffixEnd = c;
      						c--; // this gets us out of while loop.
      						break;
      					}
      				}
      			}
      		}
      		int nextEnd = nextSpaceIndex(sb, suffixEnd + 1, lastIndex + 1);
      		if (position == lastIndex) {
      			suffix = "";
      			next = "";
      		}
      		else {
      			suffix = sb.substring(position + 1, suffixEnd).trim();
      			next = sb.substring(suffixEnd + 1, nextEnd).trim();
      		}
      	}
      	
      	buf.append("x=");
    	buf.append(prefix);
    	collectFeats.add(buf.toString());
    	buf.setLength(0);
    
	    buf.append("v=");
	    buf.append(previous);
	    buf.setLength(0);
    
    	buf.append("s=");
    	buf.append(suffix);
    	collectFeats.add(buf.toString());
    	buf.setLength(0);
	    
	    buf.append("n=");
	    buf.append(next);
    	collectFeats.add(buf.toString());
    	buf.setLength(0);
    
	    String[] context = new String[collectFeats.size()];
    	context = (String[]) collectFeats.toArray(context);
    	collectFeats.clear();
    	return context;
  	}
  	
  	/**
  	 * Finds the index of the nearest space before a specified index.
   	*
   	* @param sb   The string buffer which contains the text being examined.
   	* @param seek The index to begin searching from.
   	* @return The index which contains the nearest space.
   	*/
  	private static final int previousSpaceIndex(StringBuffer sb, int seek) {
    	seek--;
    	while (seek > 0) {
      		if (sb.charAt(seek) == ' ') {
        		while (seek > 0 && sb.charAt(seek - 1) == ' ')
          			seek--;
        	return seek;
      		}
      		seek--;
    	}
    	return 0;
    }
    
    /**
   	* Finds the index of the nearest space after a specified index.
   	*
   	* @param sb The string buffer which contains the text being examined.
   	* @param seek The index to begin searching from.
   	* @param lastIndex The highest index of the StringBuffer sb.
   	* @return The index which contains the nearest space.
   	*/
  	private static final int nextSpaceIndex(StringBuffer sb, int seek, int lastIndex) {
  		seek++;
    	char c;
    	while (seek < lastIndex) {
    		c = sb.charAt(seek);
      		if (c == ' ' || c == '\n') {
        		while (sb.length() > seek + 1 && sb.charAt(seek + 1) == ' ')
          			seek++;
        	return seek;
      		}
      		seek++;
      	}
      	return lastIndex;
    }
}
