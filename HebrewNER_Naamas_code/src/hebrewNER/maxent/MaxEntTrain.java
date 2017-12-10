package hebrewNER.maxent;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import opennlp.maxent.*;
import opennlp.maxent.io.*;

/**
 * A class for training maxent model from a corpus in one training file. Uses the method 
 * trainModel of class opennlp.maxent.GIS.<br>
 * The model created is saved in a file.
 */
public class MaxEntTrain {
	
	/**
  	 * main method for training maxent and saving it into a file
   	 * Usage: MaxEntTrainNameFinder training_file model_file
   	 */
	public static void main(String[] args) throws IOException {
		if (args.length !=2) {
			System.out.println("Usage: MaxEntTrainNameFinder training_file model_file");
			System.exit(1);
		}
		try {
			EventStream es = new MaxEntEventStream(args[0]);
			GISModel mod = GIS.trainModel(100, new TwoPassDataIndexer(es, 5));
			System.out.println("Saving the model as: " + args[1]);
			File outFile = new File(args[1]);
			new SuffixSensitiveGISModelWriter(mod, outFile).persist();
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
}
