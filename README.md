<h1>Opencraft</h1>
<p>Minecraft like fait en collaboration avec Big_Bang</p>

<h2>Définition des types de données</h2>
<ul>
    <li>Byte (1 byte) -> nombre entier de -128 a 127</li>
    <li>Bool (1 byte) -> true (0x01) ou false (0x00)</li>
    <li>Char (1 byte) -> un caractaire</li>
    <li>Int (4 bytes) -> nombre entier de -2 147 483 648 a 2 147 483 647</li>
    <li>Float (4 bytes) -> nombre a virgule</li>
    <li>Type Array (taille variable)<ul>
        <li>Int : Length</li>
        <li>Byte Array : Data</li></ul>
</ul>


<h2>Définition d'un packet</h2>
<ul>
    <li>Byte : ID</li>
    <li>Data (suite de données)</li>
</ul>


<h2>Packets reçus</h2>
<h3>Server Side</h3>
<ul>
    <li>
        <h4>ConnectionPacket (0)</h4>
        <ul>
            <li>Char Array : Player Name</li>
            <li>Int : Player View Distance</li>
            <li>Int : UDP Port</li>
        </ul>
    </li>
    <li><h4>DisconnectPacket (1)</h4></li>
    <li>
        <h4>PlayerMovementPacket (2)</h4>
        <ul>
            <li>Float : Player X</li>
            <li>Float : Player Y</li>
            <li>Float : Player Z</li>
            <li>Float : Player Pitch</li>
            <li>Float : Player Yaw</li>
        </ul>
    </li>
    <li>
        <h4>ChatPacket (3)</h4>
        <ul>
            <li>Char Array : Player Message</li>
        </ul>
    </li>
    <li>
        <h4>StartBreakingPacket (4)</h4>
        <ul>
            <li>Int : Block X</li>
            <li>Int : Block Y</li>
            <li>Int : Block Z</li>
        </ul>
    </li>
    <li><h4>StopBreakingPacket (5)</h4></li>
    <li><h4>BreakBlockPacket (6)</h4></li>
    <li>
        <h4>PlaceBlockPacket (7)</h4>
        <ul>
            <li>Int : Block X</li>
            <li>Int : Block Y</li>
            <li>Int : Block Z</li>
            <li>Byte : Block Type</li>
        </ul>
    </li>
</ul>
<h3>Client Side</h3>
<ul>
    <li>
        <h4>LoginSuccessPacket (0)</h4>
        <ul>
            <li>Int : Player ID</li>
            <li>Int : Chunk to Load</li>
        </ul>
    </li>
    <li>
        <h4>JoinWorldPacket (1)</h4>
        <ul>
            <li>Float : Player X</li>
            <li>Float : Player Y</li>
            <li>Float : Player Z</li>
            <li>Float : Player Pitch</li>
            <li>Float : Player Yaw</li>
        </ul>
    </li>
    <li>
        <h4>KickPacket (2)</h4>
        <ul>
            <li>Char Array : Reason</li>
        </ul>
    </li>
    <li>
        <h4>ChatPacket (3)</h4>
        <ul>
            <li>Char Array : Player Message</li>
        </ul>
    </li>
    <li>
        <h4>ChunkUpdatePacket (4)</h4>
        <ul>
            <li>Int : Chunk X</li>
            <li>Int : Chunk Y</li>
            <li>Int : Chunk Z</li>
            <li>Byte Array : Chunk Data</li>
        </ul>
    </li>
    <li>
        <h4>BlockUpdatePacket (5)</h4>
        <ul>
            <li>Int : Block X</li>
            <li>Int : Block Y</li>
            <li>Int : Block Z</li>
            <li>Byte : Block Type</li>
        </ul>
    </li>
    <li>
        <h4>SpawnEntityPacket (6)</h4>
        <ul>
            <li>Int : Entity ID</li>
            <li>Byte : Entity Type</li>
            <li>Float : Entity X</li>
            <li>Float : Entity Y</li>
            <li>Float : Entity Z</li>
            <li>Float : Entity Pitch</li>
            <li>Float : Entity Yaw</li>
        </ul>
    </li>
    <li>
        <h4>RemoveEntityPacket (7)</h4>
        <ul>
            <li>Int : Entity ID</li>
        </ul>
    </li>
    <li>
        <h4>EntityMovementPacket (8)</h4>
        <ul>
            <li>Int : Entity ID</li>
            <li>Float : Entity X</li>
            <li>Float : Entity Y</li>
            <li>Float : Entity Z</li>
            <li>Float : Entity Pitch</li>
            <li>Float : Entity Yaw</li>
        </ul>
    </li>
</ul>

<h2>Précision sur les données des chunk</h2>
<p>
	C'est un tableau de byte (allant de -128 a 128) qui corespondent au type de chaque block du chunk<br>
	Pour connaitre l'index d'une position dans le chunk on utilise ce calcul :
</p>
<p>
	s = Taille du chunk<br>
	x = La position X du block relative au chunk<br>
	y = La position Y du block relative au chunk<br>
	z = La position Z du block relative au chunk<br>
	index = z * s² + y * s + x
</p>

<h2>Protocole de connection</h2>
<ul>
    <li>Le client envoit un ConnectionPacket (tcp)</li>
    <li>Le serveur réponde avec un LoginSuccessPacket (tcp)</li>
    <li>Le serveur envoit tous les chunks a charger (ChunkUpdatePacket en tcp)</li>
    <li>Le serveur envoit un JoinWorldPacket (tcp)</li>
    <li>Le joueur est maintenant connecté</li>
</ul>