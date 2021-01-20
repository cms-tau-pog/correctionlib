import sys; assert sys.version_info>=(3,8),"Python version must be newer than 3.8, currently %s.%s"%(sys.version_info[:2])
from typing import (
    List,
    Optional,
    Union,
    ForwardRef,
    Literal,
)
from pydantic import BaseModel, validator
def RedValueError(*args): return ValueError("\033[91m"+''.join(args)+"\033[0m")


VERSION = 1


class Model(BaseModel):
    class Config:
        extra = "forbid"


class Variable(Model):
    name: str
    type: Literal["string", "int", "real"]
    "Implicitly 64 bit integer and double-precision floating point?"
    description: Optional[str]


class Formula(Model):
    expression: str
    parser: Literal["TFormula", "numexpr"]
    parameters: List[int]
    "Index to Correction.inputs[]"


Value = Union[Formula, float]
Binning = ForwardRef("Binning")
MultiBinning = ForwardRef("MultiBinning")
Category = ForwardRef("Category")
Content = Union[Binning, MultiBinning, Category, Value]


class Binning(Model):
    nodetype: Literal["binning"]
    input: str
    edges: List[float]
    "Edges of the binning, where edges[i] <= x < edges[i+1] => f(x, ...) = content[i](...)"
    content: List[Content]
    
    @validator('edges')
    def validate_edges(cls,edges,values):
        for i, lowedge in enumerate(edges[:-1]):
          if lowedge>=edges[i+1]:
            raise RedValueError("bin edges not in increasing order: %s"%(edges))
        return edges
    
    @validator('content')
    def match_content_bins(cls,content,values):
        if 'edges' in values:
          nbins = len(values['edges'])-1
          if len(content)!=nbins:
            raise RedValueError("number of content elements (%s) must match number of bins (%s)"%(len(content),nbins))
        return content


class MultiBinning(Model):
    """N-dimensional rectangular binning"""
    nodetype: Literal["multibinning"]
    inputs: List[str]
    edges: List[List[float]]
    "Bin edges for each input"
    content: List[Content]
    
    @validator('edges')
    def match_bins_input(cls,edges,values):
        for edges_ in edges:
          for i, lowedge in enumerate(edges_[:-1]):
            if lowedge>=edges_[i+1]:
              raise RedValueError("bin edges not in increasing order: %s"%(edges_))
        if 'inputs' in values and len(edges)!=len(values['inputs']):
          raise RedValueError("number of axes (%s) must number of inputs (%s: %s)"%(len(edges),len(values['inputs']),values['inputs']))
        return edges
    
    @validator('content')
    def match_content_bins(cls,content,values):
        if 'edges' in values:
          nbins = 1
          for e in values['edges']: nbins *= len(e)-1
          if len(content)!=nbins:
            raise RedValueError("number of content elements (%s) must number of bins (%s)"%(len(content),nbins))
        return content
      


class Category(Model):
    nodetype: Literal["category"]
    input: str
    keys: List[Union[str,int]]
    content: List[Content]
    default: Content = None
    
    @validator('content')
    def match_content_key(cls,content,values):
        if 'keys' in values and len(content)!=len(values['keys']):
          raise RedValueError("number of content elements (%s) must number of keys (%s: %s)"%(len(content),len(values['keys']),values['keys']))
        return content


Binning.update_forward_refs()
MultiBinning.update_forward_refs()
Category.update_forward_refs()


class Correction(Model):
    name: str
    "A useful name"
    description: Optional[str]
    "Detailed description of the correction"
    version: int
    "Version"
    inputs: List[Variable]
    output: Variable
    data: Content


class CorrectionSet(Model):
    schema_version: Literal[VERSION]
    "Schema version"
    corrections: List[Correction]


if __name__ == "__main__":
    with open(f"data/schemav{VERSION}.json", "w") as fout:
        fout.write(CorrectionSet.schema_json(indent=4))
