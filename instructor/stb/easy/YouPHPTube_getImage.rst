.. Copyright 2022 National Technology & Engineering Solutions of Sandia, LLC
   (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
   Government retains certain rights in this software.
   
   Redistribution and use in source and binary/rendered forms, with or without
   modification, are permitted provided that the following conditions are met:
   
    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary/rendered form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.
   
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. _YouPHPTube:

YouPHPTube getImage
=======================

.. .. external

.. code-block:: php
   :linenos:

    <?php
     ...
    require_once dirname(__FILE__) . '/../videos/configuration.php';
    header('Access-Control-Allow-Origin: *');
    $url = base64_decode($_GET['base64Url']);
    $destinationFile = md5($url);
    $destination = sys_get_temp_dir().DIRECTORY_SEPARATOR.$destinationFile;
    $destinationPallet = "{$destination}palette.png";
    $cache_life = '600'; //caching time, in seconds
    $ob_flush = false;
    
    if($_GET['format'] === 'png'){
        header('Content-Type: image/x-png');
        $destination .= ".".$_GET['format'];
        $exec = "ffmpeg -i \"{$url}\" -f image2  -s 400x225 -vframes 1 -y {$destination}";
        $destinationTmpFile = "{$global['systemRootPath']}view/img/OnAir.png";
    }else if($_GET['format'] === 'jpg'){
        header('Content-Type: image/jpg');
        $destination .= ".".$_GET['format'];
        $exec = "ffmpeg -i \"{$url}\" -f image2  -s 400x225 -vframes 1 -y {$destination}";
        $destinationTmpFile = "{$global['systemRootPath']}view/img/OnAir.jpg";
    }else if($_GET['format'] === 'gif'){
        // gif image has the double lifetime
        $cache_life*=2;
        header('Content-Type: image/gif');
        $destination .= ".".$_GET['format'];    
        //Generate a palette:
        $ffmpegPallet ="ffmpeg -y -t 3 -i \"{$url}\" -vf fps=10,scale=320:-1:flags=lanczos,palettegen {$destinationPallet}";
        $exec ="ffmpeg -y -t 3 -i \"{$url}\" -i {$destinationPallet} -filter_complex \"fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse\" {$destination}";
        $destinationTmpFile = "{$global['systemRootPath']}view/img/notfound.gif";
    }else if($_GET['format'] === 'webp'){
        // gif image has the double lifetime
        $cache_life*=2;
        header('Content-Type: image/webp');
        $destination .= ".".$_GET['format'];    
        $exec ="ffmpeg -y -ss 3 -t 3 -i \"{$url}\" -vcodec libwebp -lossless 1 -vf fps=10,scale=640:-1 -q 60 -preset default -loop 0 -an -vsync 0 {$destination}";
        $destinationTmpFile = "{$global['systemRootPath']}view/img/notfound.gif";
    }else{
        error_log("ERROR Destination get Image {$_GET['format']} not suported");
        die();
    }
     ... 
    if(!file_exists($destination) || fileOlderThen($destination, $cache_life) || !empty($_GET['renew'])){
        if(!empty($ffmpegPallet)){        
            $cmd = "{$ffmpegPallet} &> /dev/null &";        
            exec($cmd);
            error_log("Create Gif Pallet: {$cmd}");        
            if(is_readable($destinationPallet)){
                $cmdGif = "{$exec} &> /dev/null &";
                exec($cmdGif);
                error_log("Create Gif with Ppallet: {$cmd}");
            }else{
                $cmdGif = "ffmpeg  -y -t 3 -i \"{$url}\" -vf fps=10,scale=320:-1 {$destination} &> /dev/null &";
                exec($cmdGif);
                error_log("Create Gif no Pallet: {$cmd}");
            }
        }else{
            $cmd = "{$exec} &> /dev/null &";
            exec($cmd);
            error_log("Exec get Image: {$cmd}");
        }
    }
   
**Context**

 * The attacker controls all of the GET parameters into this file.

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: php
       :linenos:
       :emphasize-lines: 5,15,20,28,29,36,59

       <?php
        ...
       require_once dirname(__FILE__) . '/../videos/configuration.php';
       header('Access-Control-Allow-Origin: *');
       $url = base64_decode($_GET['base64Url']);
       $destinationFile = md5($url);
       $destination = sys_get_temp_dir().DIRECTORY_SEPARATOR.$destinationFile;
       $destinationPallet = "{$destination}palette.png";
       $cache_life = '600'; //caching time, in seconds
       $ob_flush = false;
       
       if($_GET['format'] === 'png'){
           header('Content-Type: image/x-png');
           $destination .= ".".$_GET['format'];
           $exec = "ffmpeg -i \"{$url}\" -f image2  -s 400x225 -vframes 1 -y {$destination}";
           $destinationTmpFile = "{$global['systemRootPath']}view/img/OnAir.png";
       }else if($_GET['format'] === 'jpg'){
           header('Content-Type: image/jpg');
           $destination .= ".".$_GET['format'];
           $exec = "ffmpeg -i \"{$url}\" -f image2  -s 400x225 -vframes 1 -y {$destination}";
           $destinationTmpFile = "{$global['systemRootPath']}view/img/OnAir.jpg";
       }else if($_GET['format'] === 'gif'){
           // gif image has the double lifetime
           $cache_life*=2;
           header('Content-Type: image/gif');
           $destination .= ".".$_GET['format'];    
           //Generate a palette:
           $ffmpegPallet ="ffmpeg -y -t 3 -i \"{$url}\" -vf fps=10,scale=320:-1:flags=lanczos,palettegen {$destinationPallet}";
           $exec ="ffmpeg -y -t 3 -i \"{$url}\" -i {$destinationPallet} -filter_complex \"fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse\" {$destination}";
           $destinationTmpFile = "{$global['systemRootPath']}view/img/notfound.gif";
       }else if($_GET['format'] === 'webp'){
           // gif image has the double lifetime
           $cache_life*=2;
           header('Content-Type: image/webp');
           $destination .= ".".$_GET['format'];    
           $exec ="ffmpeg -y -ss 3 -t 3 -i \"{$url}\" -vcodec libwebp -lossless 1 -vf fps=10,scale=640:-1 -q 60 -preset default -loop 0 -an -vsync 0 {$destination}";
           $destinationTmpFile = "{$global['systemRootPath']}view/img/notfound.gif";
       }else{
           error_log("ERROR Destination get Image {$_GET['format']} not suported");
           die();
       }
        ... 
       if(!file_exists($destination) || fileOlderThen($destination, $cache_life) || !empty($_GET['renew'])){
           if(!empty($ffmpegPallet)){        
               $cmd = "{$ffmpegPallet} &> /dev/null &";        
               exec($cmd);
               error_log("Create Gif Pallet: {$cmd}");        
               if(is_readable($destinationPallet)){
                   $cmdGif = "{$exec} &> /dev/null &";
                   exec($cmdGif);
                   error_log("Create Gif with Ppallet: {$cmd}");
               }else{
                   $cmdGif = "ffmpeg  -y -t 3 -i \"{$url}\" -vf fps=10,scale=320:-1 {$destination} &> /dev/null &";
                   exec($cmdGif);
                   error_log("Create Gif no Pallet: {$cmd}");
               }
           }else{
               $cmd = "{$exec} &> /dev/null &";
               exec($cmd);
               error_log("Exec get Image: {$cmd}");
           }
       }


    The web page accepts as input for the ``url`` parameter any string that is possible
    to be base64 encoded.  This allows for an incredible amount of control over this variable.
    That variable is then used to construct a command that is eventually executed on the
    system resulting in a pretty easy command injection vulnerability.

    `Original article with more details
    <https://talosintelligence.com/vulnerability_reports/TALOS-2019-0917>`_
    [`cached version <../../../ref/YouPHPTube_command_injection.html>`__]


    There is another bug in this program that results in an SQL injection too.
    `SQL Injection <https://talosintelligence.com/vulnerability_reports/TALOS-2019-0941>`_
    [`cached version <../../../ref/YouPHPTube_SQL_injection.html>`__]
