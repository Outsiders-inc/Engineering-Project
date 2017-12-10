package hebrewNER.hmm;

/**
 * Event holds 3 public variable: tag, part of speach and context.
 * To be used by the event stream and the train method.
 */
public class Event{
	
	public String tag;
	public String pos;
	public String context;
		
	Event(String tag,String pos,String context){
		this.tag=tag;
		this.pos=pos;
		this.context=context;
	}
	
}