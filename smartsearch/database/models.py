from pydantic import BaseModel  
from typing import List  


# Bu sınıf, eğitimle ilgili verileri doğrulamak ve yapılandırmak için kullanılacaktır.
class Training(BaseModel):
    title: str  
    category: List[str]  
    description: str  