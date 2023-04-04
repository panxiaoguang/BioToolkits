
import pynecone as pc
from Bio import SeqIO
from urllib.request import urlopen
import pandas as pd
import os
from utils import makenames
import io
from Bio.Seq import Seq
import json as json_package

class State(pc.State):
    excel_file: str
    barcode_file: str
    _outfile:str
    _outfile2:str

    async def handle_upload(self, file: pc.UploadFile):
        upload_data = await file.read()
        outfile = f".web/public/{file.filename}"
        with open(outfile, "wb") as f:
            f.write(upload_data)
        self.excel_file = file.filename
        self._outfile = outfile
    
    async def handle_upload2(self, file: pc.UploadFile):
        upload_data = await file.read()
        outfile2 = f".web/public/{file.filename}"
        with open(outfile2, "wb") as f:
            f.write(upload_data)
        self.barcode_file = file.filename
        self._outfile2 = outfile2

class Sequence(State):
    dis:bool=True
    show: bool = False
    waiting:bool = True
    input:str=""
    output:list
    blatData:list[list]

    def change(self):
        self.show = not (self.show)
    
    def nima(self):
        self.waiting = not (self.waiting)
    
    def clean(self):
        self.input=""
        self.output=[]
        self.blatData = [[]]

    def change_dis(self,_):
        if self.input!="":
            self.dis=False
        else:
            self.dis=True
            self.waiting=True

    def complement(self):
        jieguo=[]
        for record in SeqIO.parse(io.StringIO(self.input),"fasta"):
            jieguo.append(">"+str(record.id))
            jieguo.append(str(record.seq.complement()))
        self.output = jieguo

    def rev_complement(self):
        jieguo=[]
        for record in SeqIO.parse(io.StringIO(self.input),"fasta"):
            jieguo.append(">"+str(record.id))
            jieguo.append(str(record.seq.reverse_complement()))
        self.output = jieguo

    def translate(self):
        jieguo=[]
        for record in SeqIO.parse(io.StringIO(self.input),"fasta"):
            jieguo.append(">"+str(record.id))
            jieguo.append(str(record.seq.translate()))
        self.output = jieguo

    def blat(self):
        finallyData = []
        for record in SeqIO.parse(io.StringIO(self.input),"fasta"):
            userseq = str(record.seq)
            url = f"https://genome.ucsc.edu/cgi-bin/hgBlat?userSeq={userseq}&type=DNA&db=hg38&output=json"
            r = urlopen(url)
            tmpData = json_package.load(r)['blat']
            if len(tmpData) > 0:
                for i in tmpData:
                    finallyData.append([record.id,i[13],i[15],i[16],i[8]])
        if len(finallyData) == 0:
            self.show=True
            self.blatData = [[]]
        else:
            self.waiting = True
            self.blatData = finallyData


class Excel2shell(Sequence):
    modalData:pd.DataFrame = pd.DataFrame({"sampleName":["na"],"barcode":[0],"chip":["na"],"lane":["na"],"dataPath":["na"]})
    sampleNameIndex: int = 4
    barcodeIndex: int = 23
    chipIndex: int = 27
    laneIndex: int = 28
    datapathIndex: int = 48
    remotePath: str = "10.2.100.1:/pakpox/pob8d1"
    cmd1: list[str]
    cmd2: list[str]
    show2: bool = False
    
    def getCmd(self):
        df = pd.read_excel(self._outfile)
        os.remove(self._outfile)
        df = df.iloc[:,[self.sampleNameIndex-1,self.barcodeIndex-1,self.chipIndex-1,self.laneIndex-1,self.datapathIndex-1]]
        ## change names
        df.columns = ["sampleName", "barcode", "chip", "lane", "dataPath"]
        ## if sampleName is duplicated, fix the name
        self.modalData = df
        df = makenames(df,"sampleName")
        ## make cmd
        df = df.assign(filename1=df.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"1.fq.gz"]),axis=1))
        df = df.assign(filename2=df.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"2.fq.gz"]),axis=1))
        self.cmd1 = df.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename1']) + " " + os.path.join(self.remotePath,row['sampleName'] + "_R1.fastq.gz"),axis=1).tolist()
        self.cmd2 = df.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename2']) + " " + os.path.join(self.remotePath,row['sampleName'] + "_R2.fastq.gz"),axis=1).tolist()
    
    def removename(self):
        df2 = self.modalData
        df = pd.read_excel(self._outfile2)
        os.remove(self._outfile2)
        df.columns = ["sampleName","trueName"]
        df2 = df2.merge(df,how="left",on="sampleName")
        df2 =df2.drop(columns=["sampleName"])
        df2 = df2.rename(columns={"trueName":"sampleName"})
        #remove Nan
        df2 = df2[~df2["sampleName"].isna()]
        self.modalData = df2
        df2 = makenames(df2,"sampleName")
        df2 = df2.assign(filename1=df2.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"1.fq.gz"]),axis=1))
        df2 = df2.assign(filename2=df2.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"2.fq.gz"]),axis=1))
        self.cmd1 = df2.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename1']) + " " + os.path.join(self.remotePath,row['sampleName'] + "_R1.fastq.gz"),axis=1).tolist()
        self.cmd2 = df2.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename2']) + " " + os.path.join(self.remotePath,row['sampleName'] + "_R2.fastq.gz"),axis=1).tolist()

    def change(self):
        self.show2 = not (self.show2)
