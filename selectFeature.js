inlets = 4;
outlets = 3;

var xVal = 7;
var yVal = 8;
var xFeat = 0;
var yFeat = 1;
var weights = [1., 1., 0., 0., 0., 0., 0., 0., 0., 0.];
var values = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.];

function msg_float(a)
{
	if(inlet == 0) xVal = a;
	if(inlet == 1) yVal = a;
	values[xFeat] = xVal;
	values[yFeat] = yVal;
	outlet(0, values);
}

function msg_int(a)
{
	if(inlet == 2) xFeat = a;
	if(inlet == 3) yFeat = a;

	for(i = 0; i < weights.length; i++)
	{

		if(i == xFeat || i == yFeat) weights[i] = 1.;
		else weights[i] = 0.0;
		values[i] = 0.0;
		
	}
	outlet(1, weights);
    outlet(2, xFeat, yFeat);
}