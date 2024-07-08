## Funcionamento do RSA

O RSA é um algoritmo de chaves assimétricas utilizado para realizar a cifração e decifração de informações.

Resumidamente, um algoritmo de chave assimétrica utiliza um par de chaves sendo elas: **Chave Pública** e **Chave Privada**, que são matematicamente relacionadas para que uma chave desfaça as alterações feitas pela outra.

Tipicamente a **Chave Pública** é utilizada para cifrar informações e a **Chave Privada** é utilizada para a decifração de informações.

Com isso:

- A Chave Pública pode ser compartilhada com todos os interessados na comunicação. Qualquer pessoa com a chave consegue cifrar mensagens
- A Chave Privada deve ser mantida em segurança. Somente o dententor da Chave Privada consegue decifrar as informações cifradas pela respectiva chave pública.

### Chaves do RSA

#### **Primeiro Passo (Gerando números primos):**

Tipicamente, as chaves do RSA são geradas a partir da multiplicação de dois números primos grandes, **p** e **q**.

> Neste módulo, os números primos grandes são gerados de forma pseudoaleatórias e sua primalidade é verificada através do algoritmo de Miller Rabin. [Documentação do algoritmo de Miller Rabin](api/Utils/MillerRabin.md)

#### **Segundo Passo (Calculando módulo e Totiente):**

Após gerar os números primos, é necessário computar o valor do módulo que será utilizado na cifração e decifração das informações. Para o valor do módulo temos o calculo: `n = p * q`.

Além do módulo, é necessário encontrar o valor do Totiente de Euler para **n**, ou `Phi(n)`. Este valor será utilizado para que seja possível gerar a **chave privada** posteriormente.

> A função `Phi` de um número **p** diz respeito a quantidade de valores, menores que **p** que são coprimos com o número **p**. Se **p** for primo, então `Phi(p) = p - 1`, levando em consideração que qualquer valor menor que **p** é seu coprimo.

Levando em consideração que **p** e **q** são valores primos, então o `Phi(n)` pode ser tido como `Phi(n) = (p-1) * (q-1)`.

#### **Terceiro Passo (Gerando a Chave Pública):**

É escolhido um valor inteiro para **e** que esteja no intervalo `1 ... Phi(n)`. Normalmente não é escolhido um valor grande para este inteiro para que a operação de cifração não seja lenta.

Tipicamente este valor é pré-escolhido, podendo ser igual ou superior a **65537**.

Com o valor de **e**, é possível ter a **Chave Pública** formada pelo par **(e, n)**.

>Neste módulo é possível escolher outro valor para **e**, caso não seja informado o valor Default é utilizado.

#### **Quarto Passo (Gerando a Chave Privada):**

A **Chave Privada** é gerada de forma que seja matematicamente relacionada com a **Chave Pública**.

O expoente da **Chave Privada "d",** é o inverso modular do Expoente Público **"e"** mod **Phi(n)**, ou seja:

- `(d * e) mod Phi(n) = 1`

>Neste módulo, o inverso modular é calculado a partir do método JBR desenvolvido pelo Doutor Joacil Basílio Rael. O método consiste em uma releitura do algoritmo estendido de Euclides. [Documentação do algoritmo JBR](api/Utils/JBR.md).
