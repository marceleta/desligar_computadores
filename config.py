import json

class Config():
    
    file_config = 'config.json'
    computadores = None
    
    @classmethod
    def _load_json(cls):
        with open(cls.file_config) as file:
            file_content = file.read()
        
        return json.loads(file_content)
        
    
    @classmethod
    def get_computadores(cls):
        
        if cls.computadores is None:
            _json = cls._load_json()
            cls.computadores = _json['computadores']
            
        return cls.computadores
            