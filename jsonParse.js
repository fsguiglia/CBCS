outlets = 3;
var _memstr;
var _unidades;
var _data = new Object();
var _files = [];

function setDictID(id)
{
	_unidades = new Dict(id + "-unidades");
	keys = _unidades.getkeys();
	if(keys != null)
	{
		for(i = 0; i < keys.length; i++)
		{
			var a = _unidades.get(keys[i]);
			outlet(0, a);
			
			var returnPath = true;
		
			for(j = 0; j < _files.length; j++)
			{
				if(a[10] == _files[j])
				{
					returnPath = false;
					break;
				}
			}
		
			if(returnPath)
        	{
            	outlet(1, a[10]);
            	_files.push(a[10]);
        	}
		}
    	outlet(2, "bang");
	}
	
}

function load(path)
{
	_memstr = "";
	var f = new File(path);	
	f.open();
	if (f.isopen)
	{
		while(f.position<f.eof)
		{
			_memstr+=f.readstring(800);
		}
		f.close();
	} 
	else
	{
		post("Error\n");
	}
	_data = JSON.parse(_memstr);
	
	for(i = 0; i < _data["samples"].length; i++)
	{
		var a = [
				_data["samples"][i]["bandwidth"],
				_data["samples"][i]["centroid"],
				_data["samples"][i]["flatness"],
				_data["samples"][i]["rms"],
				_data["samples"][i]["rolloff"],
                _data["samples"][i]["pca_x"],
                _data["samples"][i]["pca_y"],
                _data["samples"][i]["tsne_x"],
                _data["samples"][i]["tsne_y"],
                _data["samples"][i]["pos"],
				_data["samples"][i]["name"]
				]; 
		outlet(0, a);
		_unidades.set(String(i), a);
		
		var returnPath = true;
		
		for(j = 0; j < _files.length; j++)
		{
			if(_data["samples"][i]["name"] == _files[j])
			{
				returnPath = false;
				break;
			}
		}
		
		if(returnPath)
        {
            outlet(1, _data["samples"][i]["name"]);
            _files.push(_data["samples"][i]["name"]);
        }
	}
    outlet(2, "bang");
}

function clear()
{
	if(filers.length > 0)
	{
		_files.clear();
	}
	_unidades.clear();
}