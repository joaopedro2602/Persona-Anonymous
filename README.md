# Persona-Anonymous
Integrantes:
Edward Mevis da Silva
João Pedro Silva Cabral
Maria Eduarda Silva Werlang
<h2>📘 Contexto</h2>
<p>
O conjunto de dados utilizado nesta aplicação é uma base <strong>fictícia</strong> inspirada na série de jogos <em>Persona</em>, empregada aqui apenas como
<strong>exemplo de estrutura de dados pessoais e relacionais</strong>.
O objetivo é utilizar esse dataset de base para um aplicação quer irá anonimizar esse dados com machine learning.
</p>

<hr>

<h2>🧩 Estrutura dos Dados</h2>
<p>
O arquivo original (<code>persona_characters.json</code>) contém três grupos principais, cada um representando uma versão de um universo narrativo distinto:
</p>
<ul>
  <li><strong>Persona 3</strong></li>
  <li><strong>Persona 4</strong></li>
  <li><strong>Persona 5</strong></li>
</ul>

<p>
Cada grupo lista os personagens principais do respectivo universo, com três atributos relevantes para o processo de anonimização:
</p>

<table>
  <thead>
    <tr>
      <th>Campo</th>
      <th>Tipo</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>nome</code></td>
      <td><em>string</em></td>
      <td>Identificador textual do personagem (funciona como nome pessoal). É tratado como dado sensível e é <strong>pseudonimizado</strong> via HMAC-SHA256.</td>
    </tr>
    <tr>
      <td><code>persona</code></td>
      <td><em>array[string]</em></td>
      <td>Lista de nomes simbólicos associados ao personagem (representa arquétipos ou "máscaras" psicológicas). Este campo é utilizado como <strong>feature textual</strong> para clusterização via TF-IDF + KMeans.</td>
    </tr>
    <tr>
      <td><code>confidente</code></td>
      <td><em>string</em></td>
      <td>Categoria ou arquétipo social que representa o papel do personagem em relação a outros (semelhante a uma “classe” ou “grupo”). Este atributo é <strong>generalizado e hasheado</strong>, sendo usado também para checar o tamanho de grupos (<em>k-anonymity</em>).</td>
    </tr>
  </tbody>
</table>

<hr>

<h2>🧾 Exemplo de Registro</h2>

<pre><code>{
  "nome": "Makoto Yuki",
  "persona": ["Orpheus", "Messiah"],
  "confidente": "The Fool"
}
</code></pre>

<p>Após processamento, o registro é convertido em algo como:</p>

<pre><code>{
  "id": "e21e5b68-b1a6-47d8-be02-b43c1a38d236",
  "name_hash": "2ad58594841194c7e8f2609a57a7ba9b823...",
  "personas": "cluster_1",
  "confidente_hash": "57a36c03c4489ac035ac2c83f00fc75587b...",
  "persona_score": -0.47
}
</code></pre>

<hr>


