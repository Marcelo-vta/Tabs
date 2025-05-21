# TABS

A TABS é uma linguagem desenvolvida para músicos que querem acompanhar suas cifras. Com a TABS, é possível criar e testar as cifras, em conjunto com a lógica da programação.

## Como funciona

A linguagem utiliza tipos int e song, de forma que seja possível realizar operações entre ambos os tipos.

### Para criar uma música

Para criar uma música, o ideal é definir uma variável para esta música.

As variáveis do tipo *song* são criadas da forma:

``` NOME_DA_VARIAVEL = "|N-N-N-N-N-N|, |M-M-M-M-M-M|, ..." ```

Primeiro, note que o nome da variável de música está em letra maiúsucula. Isso é um requisito para definir variáveis do tipo *song*

O valor a ser atribuído à variável é definido da forma ` "|N-N-N-N-N-N|, |M-M-M-M-M-M|, ..." ` como exemplificado acima. Este valor é composto de diversas Tabs separadas por vírgulas. **Não é necessário atribuir um valor ao definir uma variável**.

### Tabs

As *tabs* são um componente essencial para a criação de *songs*.  
Uma *tab* é composta de um `|`, que abre a *tab*, seguido por 6 valores separados por `-`.

Cada valor pode assumir um inteiro de `0` a `30`, ou `X`. 

O valor numérico representa qual casa do violão será tocada na corda do índice do valor. Caso o valor seja `X`, a corda não será tocada.

### Exemplo de Tab

O acorde Am:

![Am](Am-1.png)

Representado em uma Tab, fica:

``` |X-0-2-2-1-0| ```

### Operações entre Songs e Números

As operações possíveis são:

- ***Song x Song***
    -   Concatenação (++): Concatena duas Songs em uma.
    -   Subtração (--): Retira da primeira Song as *tabs* presentes na segunda Song.

    -   Comparação: Comparam o tamanho de duas Songs
        - Igual a (==): Compara o conteúdo de duas Songs
        - Maior que (>)
        - Menor que (<)
        - Maior ou igual a (>=)
        - Menor ou igual a (<=)

- **Song x Number**
    -   Multiplicação (**): Concatena N vezes a Song no final dela mesma.

    -   Comparação: Comparam o tamanho da Song com o número provido
        - Igual a (==)
        - Maior que (>)
        - Menor que (<)
        - Maior ou igual a (>=)
        - Menor ou igual a (<=)

Também são possíveis operaçõoes aritiméticas entre dois números

- Adição (+)
- Subtração (-)
- Multiplicação (*)
- Divisão (/)

E operações de comparação:

- Igual a (==)
- Maior que (>)
- Menor que (<)
- Maior ou igual a (>=)
- Menor ou igual a (<=)

### Estrutura de código

Como pode ser visto no código exemplo abaixo, um código *TABS* inicia com uma chave aberta `{`,  que define o bloco principal do código.  
Após isso, existem vários tipos de statements possíveis para utilizar ao decorrer do código.

- Declaração: Define uma variável numérica ou de uma música para ser utilizada durante o código
- If: Modelo de `if (cond){}else{}` para realizar operações condicionais
- While: Modelo de `while (cond){}` para realizar operações em loop
- Print: `print(value)` para vizualizar variáveis no terminal
- Print Song: `prints(value)` para vizualizar músicas no terminal de forma mais bem-organizada
- Play: `play(song)` toca a música passada como argumento

**É necessário utilizar `;` ao final de todo statement**

### Para executar

```
    pip install -r requirements.txt

    Python Tabs_lang/main.py NOME_DO_ARQUIVO.Tabs
```

### Exemplos de código

Ambos os exemplos abaixo estão presentes nos arquivos `test.Tabs` `smoke_on_the_water.Tabs`:

``` 
{

    // Código para testar e entender as features da linguagem

    rep = get(); // get() para pegar inputs do usuário

    A = "|0-2-2-X-X-X|";
    B = "|1-3-3-X-X-X|";
    C = "|2-4-4-X-X-X|";

    SONG = "";

    i = 0;
    while (i < rep){
        SONG = SONG ++ A ++ B ++ C;
        if (i == (rep - 1) ){
            SONG = SONG ++ BLANK;
        }
        i = i + 1;
    }

    prints(SONG);

    SONG = SONG -- "|X-X-X-X-X-X|";

    prints(SONG);

    // pode ser tambem

    SONG2 = (A ++ B ++ C)**rep;

    // ou

    SONG3 = "|0-2-2-X-X-X|, |1-3-3-X-X-X|, |2-4-4-X-X-X|" ** rep;

    print(SONG == SONG2);
    print(SONG2 == SONG3);

    play(SONG3);

}
```

``` 
{

    // SMOKE ON THE WATER

    A1 = "|3-5-5-X-X-X|";
    A2 = "|6-8-8-X-X-X|";
    A3 = "|X-3-5-5-X-X|";
    A4 = "|X-4-6-6-X-X|";

    A1_B = A1 ++ BLANK;
    A2_B = A2 ++ BLANK;
    A3_B = A3 ++ BLANK;
    A4_B = A4 ++ BLANK;

    RIFF_P1 = A1_B ++ A2_B ++ A3_B ++ BLANK;
    RIFF_P2 = A1_B ++ A2_B ++ A4 ++ A3_B ++ (BLANK ** 2);

    RIFF_END = A2_B ++ A1_B;

    SONG = RIFF_P1 ++ RIFF_P2 ++ RIFF_P1 ++ RIFF_END;

    play(SONG);
}
```







