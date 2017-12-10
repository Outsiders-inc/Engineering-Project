package hebrewNER.io;


/**
 * Receives UTF8 hebrew string and tokenizes it.
 * Returns a string where 'space' delimiters between
 * the tokens
 */
 
public class Tokenizer{
	
  /**
   * Tokenize
   * @param rawData - hebrew visual string to tokenize
   * @return tokenized string
   */
   
  public static String tokenize(String rawData){
  	StringBuffer strbuf = new StringBuffer("");
    char ch;
    for(int i=0;i<rawData.length();i++){
      ch = rawData.charAt(i);
      switch(ch){
      case '!':
      case '#':
      case '$':
      case '%':
      case '&':
      case '(':
      case ')':
      case '*':
      case '+':
      case '/':
      case ':':
      case ';':
      case '<':
      case '=':
      case '>':
      case '?':
      case '@':
      case '[':
      case '\\':
      case ']':
      case '^':
      case '_':
      case '`':
      case '{':
      case '|':
      case '}':
      case '~':
      	if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
      		strbuf.append(" ");
        strbuf.append(ch);
        if (i<rawData.length()-1 && !Character.isWhitespace(rawData.charAt(i+1)))
          strbuf.append(" ");
        break;
      case '"':
      	if ((i>0 && Character.isLetter(strbuf.charAt(strbuf.length()-1))) &&
            (i<rawData.length()-1 && Character.isLetter(rawData.charAt(i+1))))
          strbuf.append(ch);
        else {
        	if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
	            strbuf.append(" ");
          	strbuf.append(ch);
          	if (i<rawData.length()-1 && !Character.isWhitespace(rawData.charAt(i+1)))
	            strbuf.append(" ");
        }
        break;
      case '\'':
        if (i>0 && Character.isLetter(strbuf.charAt(strbuf.length()-1))) // hebrew letters ???
          strbuf.append(ch);
        else {
          if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
            strbuf.append(" ");
          strbuf.append(ch);
          if (i<rawData.length()-1 && !Character.isWhitespace(rawData.charAt(i+1)))
            strbuf.append(" ");
        }
        break;
      case '-':
        if ((i>0 && Character.isLetter(strbuf.charAt(strbuf.length()-1))) &&
            (i<rawData.length()-1 && Character.isLetter(rawData.charAt(i+1))))
          strbuf.append(ch);
        else {
          if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
            strbuf.append(" ");
          strbuf.append(ch);
          if (i<rawData.length()-1 && !Character.isWhitespace(rawData.charAt(i+1)))
            strbuf.append(" ");
        }
        break;
      case '.':
        if ((i>0 && Character.isLetterOrDigit(strbuf.charAt(strbuf.length()-1))) &&
            (i<rawData.length()-1 && Character.isLetterOrDigit(rawData.charAt(i+1))))
          strbuf.append(ch);
        else {
        	if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
            	strbuf.append(" ");
          	strbuf.append(ch);
          	if (i<rawData.length()-1 && !Character.isWhitespace(rawData.charAt(i+1)))
	            strbuf.append(" ");
        }
        break;
      case ',':
        if ((i>0 && Character.isDigit(strbuf.charAt(strbuf.length()-1))) &&
            (i<rawData.length()-1 && Character.isDigit(rawData.charAt(i+1))))
          strbuf.append(ch);
        else {
          if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
            strbuf.append(" ");
          strbuf.append(ch);
          if (i<rawData.length()-1 && !Character.isWhitespace(rawData.charAt(i+1)))
            strbuf.append(" ");
        }
        break;
      default:
        if (Character.isWhitespace(ch)){
          if (i>0 && !Character.isWhitespace(strbuf.charAt(strbuf.length()-1)))
            strbuf.append(" ");
         }
         else strbuf.append(ch);
 
      }
    }
    return strbuf.toString(); 
  }
}
  
