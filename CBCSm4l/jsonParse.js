outlets = 3;
var memstr;
var data = new Object()
var files = [];

function load(path)
{
	memstr = "";
	var f = new File(path);
	f.open();
	if (f.isopen)
	{
		while(f.position<f.eof)
		{
			memstr+=f.readstring(800);
		}
		f.close();
	} 
	else
	{
		post("Error\n");
	}
	data = JSON.parse(memstr);
	
	for(i = 0; i < data["samples"].length; i++)
	{
		var a = [
				data["samples"][i]["bandwidth"],
				data["samples"][i]["centroid"],
				data["samples"][i]["flatness"],
				data["samples"][i]["rms"],
				data["samples"][i]["rolloff"],
                data["samples"][i]["pca_x"],
                data["samples"][i]["pca_y"],
                data["samples"][i]["tsne_x"],
                data["samples"][i]["tsne_y"],
                data["samples"][i]["tsne_1D"],
                data["samples"][i]["time"],
				data["samples"][i]["file"]
				]; 
		outlet(0, a);
		
		var returnPath = true;
		
		for(j = 0; j < files.length; j++)
		{
			if(data["samples"][i]["file"] == files[j])
			{
				returnPath = false;
				break;
			}
		}
		
		if(returnPath)
        {
            outlet(1, data["samples"][i]["file"]);
            files.push(data["samples"][i]["file"]);
        }
	}
    outlet(2, "bang");
}

function clear()
{
    files = [];
}