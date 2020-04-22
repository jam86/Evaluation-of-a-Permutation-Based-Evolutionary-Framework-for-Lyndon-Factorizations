import org.junit.Test;

import java.io.StringReader;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.assertEquals;

public class FastaHelperTest {
    @Test
    public void readingShouldReturnAllGenesInFasta() {
        HashMap<String, String> fasta = FastaHelper.fastaToMap(
                new StringReader(">TEST1\n123\n321\n>TEST2\n000\n333\n>TEST3\n555566"));

        for (Map.Entry<String, String> entry : fasta.entrySet()) {
            System.out.println(entry.getKey() + ":" + entry.getValue());
            assertEquals(6, entry.getValue().length());
        }
        assertEquals(3, fasta.size());
    }
}
