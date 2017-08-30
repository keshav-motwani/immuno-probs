import numpy
import string
import pylab

def multialign_genomic_templates(fastafile):
	from Bio.Align.Applications import MuscleCommandline
	from StringIO import StringIO
	from Bio import AlignIO
	
	muscle_cline = MuscleCommandline(input=fastafile)
	stdout, stderr = muscle_cline()
	multialign = AlignIO.read(StringIO(stdout), "fasta")

	return multialign


#Look for a given conserved motif in some alignments
#In the end returns the beginning position of the motif that matches most of the alignments
def find_conserved_motif(align,motif):
    motif_frac_arr = []
    for i in range(0,align.get_alignment_length()-3):
        codon_align = align[:,i:i+3]
        mask = numpy.zeros(len(align))
        for seq_rec,j in zip(codon_align,range(0,len(codon_align))):
            mask[j] = (seq_rec.seq==motif) #& (seq_rec.seq!="TGC")):
        motif_frac_arr.append(float(sum(mask))/len(codon_align))
    index = pylab.find(numpy.asarray(motif_frac_arr) == max(motif_frac_arr))
    motif_index_dict = {}
    print(index)
    for seq_rec in align:
        if(seq_rec.seq[index:index+3] == motif):

            tmp = str(seq_rec.seq[0:index])
            tmp = tmp.replace("-",'')
            #print(len(tmp))
            motif_index_dict[seq_rec.id] = len(tmp)
            test = str(seq_rec.seq)
            test = test.replace("-",'')
            print(test)
            print(test[len(tmp):len(test)])
    return motif_index_dict

def find_conserved_cystein(align):
	return find_conserved_motif(align,'TGT')

def find_conserved_tryptophan(align):
	return find_conserved_motif(align,'TGG')


def find_seq_CDR3(sequence_index,sequence,v_aligns,j_aligns,conserved_V_motif_index,conserved_J_motif_index):
        #print(sequence)
        #print(sequence_index)
        #Check whether the motif was found for the aligned gene if not return None as CDR3 sequence
        seq_v_align = v_aligns[v_aligns.seq_index==sequence_index]
        seq_v_align = seq_v_align.reset_index(drop=True)
        
        if seq_v_align.empty:
            return None
            #return "noValign"

        #print(seq_v_align)
        if not conserved_V_motif_index.has_key(seq_v_align.at[0,'gene_name']):
            return None
            #return "nomotifV"


        seq_j_align = j_aligns[j_aligns.seq_index==sequence_index]
        seq_j_align = seq_j_align.reset_index(drop=True)
        
        if seq_j_align.empty:
            return None
            #return "noJalign"
        
        #print(seq_j_align)
        if not conserved_J_motif_index.has_key(seq_j_align.at[0,'gene_name']):
            return None
            #return "nomotifJ"
            
           
        #Get the CDR3 substr including 3nt base of the motifs
        #Get first approximation based on the offset
        v_motif_index = seq_v_align.at[0,'offset'] + conserved_V_motif_index[seq_v_align.at[0,'gene_name']]
        j_motif_index = seq_j_align.at[0,'offset'] + conserved_J_motif_index[seq_j_align.at[0,'gene_name']]
        #print(v_motif_index)
        #print(j_motif_index)
        
        #Look for insertions in the left part of the alignment
        #print(type(seq_v_align.at[0,'insertions']))
        #print(asarray(seq_j_align.at[0,'insertions']))
        #print((asarray(seq_v_align.at[0,'insertions'])<v_motif_index))
        #print((asarray(seq_j_align.at[0,'insertions'])<j_motif_index))
#        if len(seq_v_align.at[0,'insertions'])!=0:
#            v_motif_index+=sum((numpy.asarray(seq_v_align.at[0,'insertions'])<v_motif_index))
#        if len(seq_j_align.at[0,'insertions'])!=0:
#            j_motif_index+=sum((numpy.asarray(seq_j_align.at[0,'insertions'])<j_motif_index))
#        #print(v_motif_index)
#        #print(j_motif_index)
#        #Look for deletions in the left part of the alignment
#        #what would happen if a nucleotide of the motif is deleted?
#        if len(seq_v_align.at[0,'deletions'])!=0:
#            v_motif_index -= sum((numpy.asarray(seq_v_align.at[0,'deletions'])<conserved_V_motif_index[seq_v_align.at[0,'gene_name']]))
#        if len(seq_j_align.at[0,'deletions'])!=0:
#            j_motif_index -= sum((numpy.asarray(seq_j_align.at[0,'deletions'])<conserved_J_motif_index[seq_j_align.at[0,'gene_name']]))
        #print(v_motif_index)
        #print(j_motif_index)
        #Check whether the two conserved motifs have not been deleted???
        end_seq = sequence[v_motif_index:j_motif_index+3]
        if (end_seq[0:3]!="TGT")&(end_seq[0:3]!="TGG"):
            #return None
            #return "TGT not found"
		return end_seq
        if end_seq[len(end_seq)-3:len(end_seq)]!="TGG":
            return None
            #return "TGG not found"
            #return end_seq
        
        #return end_seq
        return None


def find_seqs_CDR3(indexed_sequences,v_aligns,j_aligns,conserved_V_motif_index,conserved_J_motif_index):
	return indexed_sequences.apply(lambda x: find_seq_CDR3(x.seq_index,x.sequence,v_aligns,j_aligns,conserved_V_motif_index,conserved_J_motif_index),axis=1)
		
		





