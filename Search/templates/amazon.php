<?php
function ItemSearch($Keywords){
   
// Your Access Key ID, as taken from the Your Account page
$access_key_id = "AKIAIQZFRBDXW75JHSWQ";

// Your Secret Key corresponding to the above ID, as taken from the Your Account page
$secret_key = "tb10Hhd88+o+jVlaa8tISa+NW6ILIJismsnHn/Xq";

// The region you are interested in
$endpoint = "webservices.amazon.com";

$uri = "/onca/xml";

$params = array(
    "Service" => "AWSECommerceService",
    "Operation" => "ItemSearch",
    "AWSAccessKeyId" => "AKIAIQZFRBDXW75JHSWQ",
    "AssociateTag" => "loy05-20",
    "SearchIndex" => "HealthPersonalCare",
    "Keywords" => $Keywords,
    "ResponseGroup" => "Images,ItemAttributes,Offers"
);

// Set current timestamp if not set
if (!isset($params["Timestamp"])) {
    $params["Timestamp"] = gmdate('Y-m-d\TH:i:s\Z');
}

// Sort the parameters by key
ksort($params);

$pairs = array();

foreach ($params as $key => $value) {
    array_push($pairs, rawurlencode($key)."=".rawurlencode($value));
}

// Generate the canonical query
$canonical_query_string = join("&", $pairs);

// Generate the string to be signed
$string_to_sign = "GET\n".$endpoint."\n".$uri."\n".$canonical_query_string;

// Generate the signature required by the Product Advertising API
$signature = base64_encode(hash_hmac("sha256", $string_to_sign, $secret_key, true));

// Generate the signed URL
$request_url = 'http://'.$endpoint.$uri.'?'.$canonical_query_string.'&Signature='.rawurlencode($signature);

echo "Signed URL: \"".$request_url."\"";}
// $url = generateURL($asin);
// $responseXML = file_get_contents($url);
// $parsedXML = simplexml_load_string($responseXML);}

?>
