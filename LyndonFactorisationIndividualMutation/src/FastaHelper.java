import java.io.*;
import java.util.HashMap;

/**
 * Read fasta format files to hashmaps
 */
public class FastaHelper {

    /**
     * Read a fasta file and return a map of gene names and proteins
     * @param _reader A reader instance of an open file
     * @return A hashmap of gene names and proteins
     */
    public static HashMap<String, String> fastaToMap(Reader _reader) {
        BufferedReader reader = new BufferedReader(_reader);
        HashMap<String, String> out = new HashMap<>();
        try {
            String read;
            String proteinName = "";
            String buf = "";
            boolean collecting = false;
            while ((read = reader.readLine()) != null) {
                if (read.startsWith(">")) {
                    if (collecting) {
                        out.put(proteinName, buf);
                    }

                    collecting = true;
                    proteinName = read.substring(1);
                    buf = "";
                } else {
                    buf += read;
                }
            }
            out.put(proteinName, buf);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return out;
    }
}
