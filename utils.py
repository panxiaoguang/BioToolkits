import pynecone as pc
import pandas as pd
def maketd(blat_result:list):
    return pc.tr(
            pc.td(blat_result[0]),
            pc.td(blat_result[1]),
            pc.td(blat_result[2]),
            pc.td(blat_result[3]),
            pc.td(blat_result[4]),
        )

def format_output(textOut:str):
    return pc.text(textOut)

def makenames(df:pd.DataFrame,col:str)->pd.DataFrame:
    s='_'+df.groupby(col).cumcount().add(1).astype(str)
    df.loc[:,col]+=s.mask(s=="_1","")
    return df

def makeOut(cmd:str):
    return pc.text(cmd,color="#f2ad85",white_space="nowrap")

def navbar():
    return pc.hstack(
            pc.link(pc.heading("Bio's Toolkits",size="lg"),href="/"),
            pc.spacer(),
            pc.menu(
                pc.hstack(pc.menu_button("Tools",
                                         pc.icon(tag="chevron_down"),
                                         fontSize="1.2em",
                                         color="#999999",
                                         _hover={"color":"rgb(107,99,246)"},)),
                pc.menu_list(
                        pc.link(pc.menu_item("Sequence tools"),href="/seuquencetools"),
                        pc.link(pc.menu_item("Excel2Shell"),href="/excel2shell"),
                        
                        ),
                    ),
        bg="#DFE9F2",
        backdropFilter='auto',
        backdropBlur='10px',
        padding_y=["0.8em", "0.8em", "0.5em"],
        padding_x="3em",
        border_bottom="0.05em solid rgba(100, 116, 139, .2)",
        position="sticky",
        width="100%",
        top="0px",
        z_index="99",
        align_items="left",
        )
