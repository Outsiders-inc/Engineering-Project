package hebrewNER.sentenceDetect;

import java.util.ArrayList;
import java.util.List;

import opennlp.maxent.IntegerPool;

/**
 * This simple end of sentence scanner scans for <tt>. ? ! ) and "</tt>.
 */

public class EndOfSentenceScanner{
	
	public static final IntegerPool INT_POOL = new IntegerPool(500);
	public static final char[] eosCharacters =  {'.','?','!'};
	
	
	/**
     * Creates a new <code>DefaultEndOfSentenceScanner</code> instance.
     */
    public EndOfSentenceScanner() {
    }
    
    /**
     * Scans `s' for sentence ending characters and
     * returns their offsets.
     * @param s a <code>String</code> value
     * @return a <code>List</code> of Integer objects.
     */
    public List getPositions(String s) {
     	return getPositions(s.toCharArray());
    }
    
    /**
     * Scans `buf' for sentence ending characters and
     * returns their offsets.
     * @param buf a <code>StringBuffer</code> value
     * @return a <code>List</code> of Integer objects.
     */
    public List getPositions(StringBuffer buf) {
    	return getPositions(buf.toString().toCharArray());
    }
    
    /**
     * Scans `cbuf' for sentence ending characters and
     * returns their offsets.
     *
     * @param cbuf a <code>char[]</code> value
     * @return a <code>List</code> of Integer objects.
     */
    public List getPositions(char[] cbuf) {
        List l = new ArrayList();
        for (int i = 0; i < cbuf.length; i++) {
            switch (cbuf[i]) {
            case '.':
            case '?':
            case '!':
                l.add(INT_POOL.get(i));
                break;
            default:
                break;
            }
        }
        return l;
    }
}
